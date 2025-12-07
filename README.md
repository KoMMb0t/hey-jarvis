# 🎯 Hey Jarvis: Wake-Word Training Infrastructure

**Complete infrastructure for training and deploying custom wake-word models for the Computer-Voice-Assi project.**

## 🎤 Project Goal

Train a custom **"Computer"** wake-word (inspired by Star Trek) to replace the current placeholder "hey_jarvis" model. This repository contains all the tools, scripts, and infrastructure needed to collect data, train models, and deploy them to the main voice assistant.

## 🏗️ Infrastructure Components

### 1. Data Collection
- **Recording scripts** for capturing positive samples ("Computer")
- **Negative sample collection** (other words, background noise)
- **Data augmentation** tools (mixing, noise addition, speed variation)

### 2. Model Training
- Support for **OpenWakeWord** training pipeline
- Support for **Porcupine** custom wake-word creation
- Automated preprocessing and validation

### 3. Deployment
- **PyInstaller** configuration for standalone `.exe` builds
- Secure API key management with `.env` files
- Build scripts for easy distribution

## 📁 Repository Structure

```
hey-jarvis/
├── data/                    # Training data
│   ├── positive/           # "Computer" recordings
│   ├── negative/           # Other words, non-wake-word speech
│   └── background/         # Background noise samples
├── scripts/
│   ├── recording/          # Audio recording tools
│   ├── preprocessing/      # Data preparation and augmentation
│   └── training/           # Model training scripts
├── wake_word/
│   ├── recordings/         # Raw recordings
│   ├── models/            # Trained wake-word models
│   └── training/          # Training configurations and logs
├── docs/                   # Documentation
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Windows 11 (primary target platform)
- Microphone for recording samples

### Development Environment

Set up a local development environment with the provided helper scripts:

```bash
# Linux/macOS
chmod +x scripts/setup_dev_env.sh
./scripts/setup_dev_env.sh
source .venv/bin/activate
```

```powershell
# Windows PowerShell
powershell -ExecutionPolicy Bypass -File scripts/setup_dev_env.ps1
.\.venv\Scripts\Activate.ps1
```

Use the `PYTHON` environment variable to point to a specific Python executable if needed (for example, `PYTHON=python3.11 ./scripts/setup_dev_env.sh`).

### Installation

```bash
# Clone the repository
git clone https://github.com/KoMMb0t/hey-jarvis.git
cd hey-jarvis

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Recording Wake-Word Samples

```bash
# Record positive samples
python scripts/recording/record_wake_word.py --mode positive --count 200

# Record negative samples
python scripts/recording/record_wake_word.py --mode negative --count 200
```

### Training the Model

```bash
# Preprocess data
python scripts/preprocessing/prepare_datasets.py

# Train OpenWakeWord model
python scripts/training/train_openwakeword.py

# Or use Porcupine Console (see docs)
```

## 🎯 Training Goals

| Sample Type | Target Count | Purpose |
| :--- | :--- | :--- |
| **Positive Samples** | 200+ | "Computer" spoken in various ways |
| **Negative Samples** | 200+ | Other words, similar sounds |
| **Background Noise** | 60+ | Environmental sounds, music, TV |

## 🔗 Related Repositories

- **[Computer-Voice-Assi](https://github.com/KoMMb0t/Computer-Voice-Assi)** - Main voice assistant
- **[voice-assi-nexus](https://github.com/KoMMb0t/voice-assi-nexus)** - AI coordination hub

## 📊 Current Status

- ✅ Repository structure created
- 🔄 Recording scripts (in development)
- 📋 Training pipeline (planned)
- 📋 Deployment tools (planned)

## 📝 License

Part of the Computer-Voice-Assi project ecosystem.

---

**"Computer, activate voice assistant."** 🖖
