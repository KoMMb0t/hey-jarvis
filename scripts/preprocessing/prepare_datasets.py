"""
Data Preparation Script for Wake-Word Training
==============================================

This script downloads and prepares public datasets for wake-word training:
- Background noise samples
- Negative speech samples
- Organizes data structure for training

Author: Manus AI (Operation Nexus)
"""

import os
import urllib.request
import zipfile
import tarfile
from pathlib import Path
from typing import List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class DatasetPreparer:
    """Handles downloading and preparing datasets for wake-word training."""
    
    def __init__(self, base_dir: str = "../../data"):
        """
        Initialize the dataset preparer.
        
        Args:
            base_dir: Base directory for storing datasets
        """
        self.base_dir = Path(base_dir)
        self.positive_dir = self.base_dir / "positive"
        self.negative_dir = self.base_dir / "negative"
        self.background_dir = self.base_dir / "background"
        
        # Create directories
        for directory in [self.positive_dir, self.negative_dir, self.background_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def download_file(self, url: str, destination: Path) -> bool:
        """
        Download a file from URL to destination.
        
        Args:
            url: URL to download from
            destination: Local file path to save to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Downloading {url}...")
            urllib.request.urlretrieve(url, destination)
            logger.info(f"✓ Downloaded to {destination}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to download {url}: {e}")
            return False
    
    def extract_archive(self, archive_path: Path, extract_to: Path) -> bool:
        """
        Extract a zip or tar archive.
        
        Args:
            archive_path: Path to archive file
            extract_to: Directory to extract to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Extracting {archive_path.name}...")
            
            if archive_path.suffix == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
            elif archive_path.suffix in ['.tar', '.gz', '.tgz']:
                with tarfile.open(archive_path, 'r:*') as tar_ref:
                    tar_ref.extractall(extract_to)
            else:
                logger.error(f"Unknown archive format: {archive_path.suffix}")
                return False
            
            logger.info(f"✓ Extracted to {extract_to}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to extract {archive_path}: {e}")
            return False
    
    def download_background_noise(self) -> bool:
        """
        Download background noise dataset from Google's Speech Commands.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("=== Downloading Background Noise Dataset ===")
        
        # Google Speech Commands background noise
        url = "http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz"
        archive_path = self.background_dir / "speech_commands_v0.02.tar.gz"
        
        if not self.download_file(url, archive_path):
            return False
        
        if not self.extract_archive(archive_path, self.background_dir):
            return False
        
        # Clean up archive
        archive_path.unlink()
        logger.info("✓ Background noise dataset ready")
        return True
    
    def download_negative_samples(self) -> bool:
        """
        Download negative speech samples (common words dataset).
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("=== Downloading Negative Speech Samples ===")
        
        # Use Google Speech Commands for negative samples
        # (words like "yes", "no", "up", "down", etc.)
        url = "http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz"
        archive_path = self.negative_dir / "speech_commands_v0.02.tar.gz"
        
        if not self.download_file(url, archive_path):
            return False
        
        if not self.extract_archive(archive_path, self.negative_dir):
            return False
        
        # Clean up archive
        archive_path.unlink()
        logger.info("✓ Negative samples dataset ready")
        return True
    
    def verify_structure(self) -> None:
        """Verify and report on the data directory structure."""
        logger.info("=== Verifying Data Structure ===")
        
        for directory in [self.positive_dir, self.negative_dir, self.background_dir]:
            if directory.exists():
                file_count = len(list(directory.rglob("*.wav")))
                logger.info(f"✓ {directory.name}: {file_count} WAV files")
            else:
                logger.warning(f"✗ {directory.name}: Directory not found")
    
    def prepare_all(self) -> None:
        """Execute full data preparation pipeline."""
        logger.info("=" * 50)
        logger.info("WAKE-WORD DATA PREPARATION")
        logger.info("=" * 50)
        
        # Download datasets
        self.download_background_noise()
        self.download_negative_samples()
        
        # Verify structure
        self.verify_structure()
        
        logger.info("=" * 50)
        logger.info("✓ Data preparation complete!")
        logger.info("=" * 50)
        logger.info("\nNext steps:")
        logger.info("1. Record your positive samples: python ../recording/record_wake_word.py")
        logger.info("2. Run data augmentation: python augment_data.py")
        logger.info("3. Train your model: python ../training/train_openwakeword.py")


def main():
    """Main entry point."""
    preparer = DatasetPreparer()
    preparer.prepare_all()


if __name__ == "__main__":
    main()
