"""
Secure Configuration Management
================================

This module handles secure loading and management of API keys and sensitive
configuration data using environment variables.

Author: Manus AI (Operation Nexus)
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import logging

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    logging.warning("python-dotenv not installed. Install with: pip install python-dotenv")


class SecureConfig:
    """Manages secure configuration and API keys."""
    
    def __init__(self, env_file: Optional[str] = ".env"):
        """
        Initialize secure configuration.
        
        Args:
            env_file: Path to .env file (relative to project root)
        """
        self.config: Dict[str, Any] = {}
        self._loaded = False
        
        # Try to load .env file if dotenv is available
        if DOTENV_AVAILABLE and env_file:
            env_path = Path(env_file)
            if env_path.exists():
                load_dotenv(env_path)
                self._loaded = True
                logging.info(f"✓ Loaded environment from {env_path}")
            else:
                logging.warning(f"⚠ .env file not found at {env_path}")
        
        # Load configuration from environment
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from environment variables."""
        # API Keys
        self.config['openai_api_key'] = os.getenv('OPENAI_API_KEY')
        self.config['porcupine_access_key'] = os.getenv('PORCUPINE_ACCESS_KEY')
        self.config['elevenlabs_api_key'] = os.getenv('ELEVENLABS_API_KEY')
        
        # Voice Assistant Settings
        self.config['wake_word'] = os.getenv('WAKE_WORD', 'computer')
        self.config['tts_voice'] = os.getenv('TTS_VOICE', 'de-DE-KatjaNeural')
        self.config['stt_model'] = os.getenv('STT_MODEL', 'de')
        
        # Audio Settings
        self.config['sample_rate'] = int(os.getenv('SAMPLE_RATE', '16000'))
        self.config['chunk_samples'] = int(os.getenv('CHUNK_SAMPLES', '1280'))
        self.config['silence_timeout'] = float(os.getenv('SILENCE_TIMEOUT', '2.0'))
        
        # Model Paths
        self.config['wake_word_model_path'] = os.getenv('WAKE_WORD_MODEL_PATH', 'models/computer.ppn')
        self.config['vosk_model_path'] = os.getenv('VOSK_MODEL_PATH', 'models/vosk-model-de')
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    def get_required(self, key: str) -> Any:
        """
        Get required configuration value. Raises error if not found.
        
        Args:
            key: Configuration key
            
        Returns:
            Configuration value
            
        Raises:
            ValueError: If required key is not found
        """
        value = self.config.get(key)
        if value is None:
            raise ValueError(
                f"Required configuration '{key}' not found. "
                f"Please set it in .env file or environment variables."
            )
        return value
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """
        Validate that required API keys are present.
        
        Returns:
            Dictionary mapping API key names to their availability status
        """
        api_keys = {
            'OpenAI': self.config.get('openai_api_key') is not None,
            'Porcupine': self.config.get('porcupine_access_key') is not None,
            'ElevenLabs': self.config.get('elevenlabs_api_key') is not None,
        }
        return api_keys
    
    def print_status(self) -> None:
        """Print configuration status (without revealing sensitive data)."""
        print("=" * 50)
        print("SECURE CONFIGURATION STATUS")
        print("=" * 50)
        
        if self._loaded:
            print("✓ .env file loaded")
        else:
            print("⚠ No .env file found (using environment variables)")
        
        print("\nAPI Keys:")
        for name, available in self.validate_api_keys().items():
            status = "✓ Available" if available else "✗ Missing"
            print(f"  {name}: {status}")
        
        print("\nVoice Assistant Settings:")
        print(f"  Wake Word: {self.config['wake_word']}")
        print(f"  TTS Voice: {self.config['tts_voice']}")
        print(f"  STT Model: {self.config['stt_model']}")
        
        print("\nAudio Settings:")
        print(f"  Sample Rate: {self.config['sample_rate']} Hz")
        print(f"  Chunk Size: {self.config['chunk_samples']} samples")
        print(f"  Silence Timeout: {self.config['silence_timeout']}s")
        
        print("=" * 50)


# Global configuration instance
_config_instance: Optional[SecureConfig] = None


def get_config() -> SecureConfig:
    """
    Get global configuration instance (singleton pattern).
    
    Returns:
        SecureConfig instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = SecureConfig()
    return _config_instance


def main():
    """Test configuration loading."""
    config = get_config()
    config.print_status()


if __name__ == "__main__":
    main()
