# Deployment Guide

This guide explains how to build and deploy the Computer Voice Assistant as a standalone Windows executable.

## Prerequisites

Before building, ensure you have:

- **Python 3.11+** installed on Windows
- **All project dependencies** installed (see `requirements.txt`)
- **Trained wake-word model** in the `models/` directory
- **PyInstaller** installed (`pip install pyinstaller`)

## Building the Executable

### Option 1: Using the Build Script (Recommended)

The easiest way to build the executable is using the provided batch script:

```bash
build.bat
```

This script will automatically:
1. Check for Python installation
2. Create a virtual environment (if needed)
3. Install all dependencies
4. Clean previous builds
5. Run PyInstaller with the correct configuration
6. Create a standalone executable in the `dist/` directory

### Option 2: Manual Build

If you prefer to build manually:

```bash
# Activate virtual environment
.venv\Scripts\activate

# Install PyInstaller
pip install pyinstaller

# Build with spec file
pyinstaller build.spec
```

## Build Output

After a successful build, you will find:

```
dist/
└── ComputerVoiceAssi.exe    # Standalone executable (~150-200 MB)
```

The executable includes:
- All Python dependencies
- Wake-word detection models
- Speech recognition models
- Required DLL files

## Distribution Checklist

Before distributing the executable to end users:

### 1. Prepare Distribution Package

Create a distribution folder with:

```
ComputerVoiceAssi-v1.0/
├── ComputerVoiceAssi.exe    # The executable
├── .env.example             # Configuration template
├── README.md                # User documentation
└── models/                  # Pre-trained models (optional)
    ├── computer.ppn         # Wake-word model
    └── vosk-model-de/       # STT model (if distributing)
```

### 2. Security Check

- [ ] Ensure no API keys are embedded in the executable
- [ ] Verify `.env` file is NOT included (users must create their own)
- [ ] Check that sensitive data is not in the distribution

### 3. Testing

Test the executable on a clean Windows machine:

- [ ] Runs without Python installed
- [ ] Loads configuration from `.env` file correctly
- [ ] Wake-word detection works
- [ ] Speech recognition works
- [ ] TTS output works
- [ ] All commands execute properly

### 4. Documentation

Provide clear instructions for end users:

- How to obtain required API keys
- How to create and configure `.env` file
- How to run the executable
- Troubleshooting common issues

## Configuration for End Users

Users must create a `.env` file in the same directory as the executable:

1. **Copy the example:**
   ```bash
   copy .env.example .env
   ```

2. **Edit with their API keys:**
   ```
   OPENAI_API_KEY=sk-...
   PORCUPINE_ACCESS_KEY=...
   ```

3. **Run the executable:**
   ```bash
   ComputerVoiceAssi.exe
   ```

## Customizing the Build

### Changing the Icon

Replace `assets/icon.ico` with your custom icon, then rebuild:

```python
# In build.spec
icon='assets/your_icon.ico'
```

### Hiding the Console Window

For a GUI-only version without console window:

```python
# In build.spec
console=False  # Change from True to False
```

### Including Additional Files

Add more data files to the build:

```python
# In build.spec
datas = [
    ('models', 'models'),
    ('assets', 'assets'),
    ('your_file.txt', '.'),
]
```

## Troubleshooting Build Issues

### "Module not found" errors

Add missing modules to `hiddenimports` in `build.spec`:

```python
hiddenimports = [
    'openwakeword',
    'your_missing_module',
]
```

### Executable is too large

The executable size is typically 150-200 MB due to included dependencies. To reduce size:

1. **Use UPX compression** (already enabled in `build.spec`)
2. **Exclude unused modules** in `build.spec`
3. **Don't bundle large model files** - have users download separately

### Antivirus False Positives

Some antivirus software may flag PyInstaller executables as suspicious. This is a known issue. To mitigate:

1. **Code sign your executable** with a valid certificate
2. **Submit to antivirus vendors** for whitelisting
3. **Provide source code** so users can build themselves

## Advanced: Code Signing

For professional distribution, consider code signing:

```bash
# Using signtool (Windows SDK)
signtool sign /f certificate.pfx /p password /t http://timestamp.server.com ComputerVoiceAssi.exe
```

Benefits of code signing:
- Reduces antivirus false positives
- Shows verified publisher name
- Increases user trust

## Continuous Integration

For automated builds, integrate with GitHub Actions:

```yaml
# .github/workflows/build.yml
name: Build Executable
on: [push, release]
jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pip install pyinstaller
      - run: pyinstaller build.spec
      - uses: actions/upload-artifact@v2
        with:
          name: executable
          path: dist/ComputerVoiceAssi.exe
```

## Support

For build issues or questions:
- **GitHub Issues:** https://github.com/KoMMb0t/hey-jarvis/issues
- **Email:** kommuniverse@gmail.com

---

**Happy deploying!** 🚀
