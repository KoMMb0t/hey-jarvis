"""
Data Augmentation Script for Wake-Word Training
===============================================

This script augments audio samples with various transformations:
- Add background noise
- Adjust volume
- Change speed/pitch
- Time stretching

Author: Manus AI (Operation Nexus)
"""

import os
import numpy as np
import soundfile as sf
from pathlib import Path
from typing import Tuple, List
import logging
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class AudioAugmenter:
    """Handles audio augmentation for wake-word training data."""
    
    def __init__(self, data_dir: str = "../../data"):
        """
        Initialize the audio augmenter.
        
        Args:
            data_dir: Base directory containing audio data
        """
        self.data_dir = Path(data_dir)
        self.positive_dir = self.data_dir / "positive"
        self.background_dir = self.data_dir / "background"
        self.augmented_dir = self.data_dir / "augmented"
        
        # Create augmented directory
        self.augmented_dir.mkdir(parents=True, exist_ok=True)
    
    def load_audio(self, file_path: Path) -> Tuple[np.ndarray, int]:
        """
        Load audio file.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            data, sr = sf.read(file_path)
            return data, sr
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {e}")
            return None, None
    
    def save_audio(self, audio: np.ndarray, sample_rate: int, output_path: Path) -> bool:
        """
        Save audio to file.
        
        Args:
            audio: Audio data as numpy array
            sample_rate: Sample rate in Hz
            output_path: Path to save audio file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            sf.write(output_path, audio, sample_rate)
            return True
        except Exception as e:
            logger.error(f"Failed to save {output_path}: {e}")
            return False
    
    def add_noise(self, audio: np.ndarray, noise: np.ndarray, snr_db: float = 10.0) -> np.ndarray:
        """
        Add background noise to audio with specified SNR.
        
        Args:
            audio: Clean audio signal
            noise: Noise signal
            snr_db: Signal-to-noise ratio in dB
            
        Returns:
            Audio with added noise
        """
        # Ensure noise is same length as audio
        if len(noise) < len(audio):
            # Repeat noise if too short
            repeats = int(np.ceil(len(audio) / len(noise)))
            noise = np.tile(noise, repeats)[:len(audio)]
        else:
            # Trim noise if too long
            start = random.randint(0, len(noise) - len(audio))
            noise = noise[start:start + len(audio)]
        
        # Calculate signal and noise power
        signal_power = np.mean(audio ** 2)
        noise_power = np.mean(noise ** 2)
        
        # Calculate required noise scaling factor
        snr_linear = 10 ** (snr_db / 10.0)
        scale = np.sqrt(signal_power / (snr_linear * noise_power))
        
        # Add scaled noise to signal
        return audio + scale * noise
    
    def change_volume(self, audio: np.ndarray, factor: float) -> np.ndarray:
        """
        Change audio volume.
        
        Args:
            audio: Audio signal
            factor: Volume multiplier (0.5 = half volume, 2.0 = double volume)
            
        Returns:
            Audio with adjusted volume
        """
        return audio * factor
    
    def time_stretch(self, audio: np.ndarray, rate: float) -> np.ndarray:
        """
        Stretch or compress audio in time.
        
        Args:
            audio: Audio signal
            rate: Stretch factor (0.8 = slower, 1.2 = faster)
            
        Returns:
            Time-stretched audio
        """
        # Simple time stretching via resampling
        indices = np.arange(0, len(audio), rate)
        indices = indices[indices < len(audio)].astype(int)
        return audio[indices]
    
    def augment_sample(self, audio_path: Path, background_files: List[Path], 
                      output_prefix: str) -> int:
        """
        Create multiple augmented versions of a single audio sample.
        
        Args:
            audio_path: Path to original audio file
            background_files: List of background noise files
            output_prefix: Prefix for output filenames
            
        Returns:
            Number of augmented samples created
        """
        audio, sr = self.load_audio(audio_path)
        if audio is None:
            return 0
        
        count = 0
        base_name = audio_path.stem
        
        # Original (copy)
        output_path = self.augmented_dir / f"{output_prefix}_{base_name}_original.wav"
        if self.save_audio(audio, sr, output_path):
            count += 1
        
        # Volume variations
        for vol_factor in [0.7, 1.3]:
            augmented = self.change_volume(audio, vol_factor)
            output_path = self.augmented_dir / f"{output_prefix}_{base_name}_vol{vol_factor}.wav"
            if self.save_audio(augmented, sr, output_path):
                count += 1
        
        # Speed variations
        for speed_factor in [0.9, 1.1]:
            augmented = self.time_stretch(audio, speed_factor)
            output_path = self.augmented_dir / f"{output_prefix}_{base_name}_speed{speed_factor}.wav"
            if self.save_audio(augmented, sr, output_path):
                count += 1
        
        # Add background noise (if available)
        if background_files:
            for i, bg_file in enumerate(random.sample(background_files, min(3, len(background_files)))):
                noise, noise_sr = self.load_audio(bg_file)
                if noise is not None:
                    # Resample noise if needed
                    if noise_sr != sr:
                        # Simple resampling (for production, use librosa.resample)
                        noise = np.interp(
                            np.linspace(0, len(noise), int(len(noise) * sr / noise_sr)),
                            np.arange(len(noise)),
                            noise
                        )
                    
                    augmented = self.add_noise(audio, noise, snr_db=15.0)
                    output_path = self.augmented_dir / f"{output_prefix}_{base_name}_noise{i}.wav"
                    if self.save_audio(augmented, sr, output_path):
                        count += 1
        
        return count
    
    def augment_all(self) -> None:
        """Augment all positive samples."""
        logger.info("=" * 50)
        logger.info("AUDIO DATA AUGMENTATION")
        logger.info("=" * 50)
        
        # Get all positive samples
        positive_files = list(self.positive_dir.glob("*.wav"))
        logger.info(f"Found {len(positive_files)} positive samples")
        
        # Get background noise files
        background_files = list(self.background_dir.rglob("*.wav"))
        logger.info(f"Found {len(background_files)} background noise files")
        
        if not positive_files:
            logger.error("No positive samples found! Please record samples first.")
            return
        
        # Augment each sample
        total_augmented = 0
        for i, audio_file in enumerate(positive_files, 1):
            logger.info(f"Augmenting {i}/{len(positive_files)}: {audio_file.name}")
            count = self.augment_sample(audio_file, background_files, "aug")
            total_augmented += count
            logger.info(f"  → Created {count} variations")
        
        logger.info("=" * 50)
        logger.info(f"✓ Augmentation complete!")
        logger.info(f"  Original samples: {len(positive_files)}")
        logger.info(f"  Augmented samples: {total_augmented}")
        logger.info(f"  Total dataset size: {len(positive_files) + total_augmented}")
        logger.info("=" * 50)


def main():
    """Main entry point."""
    augmenter = AudioAugmenter()
    augmenter.augment_all()


if __name__ == "__main__":
    main()
