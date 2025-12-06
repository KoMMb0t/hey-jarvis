# Security Best Practices

This document outlines security best practices for the Hey Jarvis project, particularly regarding API key management and sensitive data handling.

## API Key Management

### Never Commit Secrets to Git

**Critical:** Never commit API keys, passwords, or other sensitive data to version control. Always use environment variables or `.env` files that are excluded from Git.

### Using .env Files

The project uses `.env` files to store sensitive configuration. Follow these steps to set up secure configuration:

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your actual API keys:**
   ```bash
   notepad .env  # Windows
   ```

3. **Verify `.env` is in `.gitignore`:**
   The `.env` file should already be excluded from Git. Verify by checking `.gitignore`:
   ```
   .env
   *.env
   !.env.example
   ```

### Required API Keys

The project may require the following API keys depending on which features you use:

| Service | Required For | How to Obtain |
| :--- | :--- | :--- |
| **OpenAI** | LLM integration (ChatGPT) | https://platform.openai.com/api-keys |
| **Porcupine** | Custom wake-word (alternative) | https://console.picovoice.ai/ |
| **ElevenLabs** | Premium TTS (optional) | https://elevenlabs.io/ |

### Loading Configuration Securely

The `secure_config.py` module handles secure loading of configuration:

```python
from secure_config import get_config

config = get_config()
api_key = config.get_required('openai_api_key')
```

This approach ensures:
- API keys are never hardcoded in source files
- Missing required keys raise clear error messages
- Configuration can be validated before use

## Deployment Security

### Building Standalone Executables

When building standalone `.exe` files with PyInstaller, be aware that:

1. **API keys in `.env` files are NOT included in the executable** (by design)
2. Users must provide their own `.env` file alongside the executable
3. Never distribute executables with embedded API keys

### Recommended Distribution Approach

For distributing to end users:

1. **Distribute the executable without API keys**
2. **Include `.env.example` file**
3. **Provide clear instructions** for users to obtain and configure their own API keys
4. **Consider using local-only models** (Vosk, OpenWakeWord) to minimize API key requirements

## Data Privacy

### Audio Data

- **Recordings are stored locally** in the `data/` directory
- **Never upload user recordings** to public repositories or cloud storage without explicit consent
- **Delete recordings** after model training if they contain sensitive information

### Voice Commands

- **Local processing preferred:** Use Vosk (offline STT) when possible
- **Cloud APIs:** When using cloud APIs (OpenAI, ElevenLabs), be aware that audio/text is sent to external servers
- **User consent:** Inform users if their voice data will be processed by cloud services

## Reporting Security Issues

If you discover a security vulnerability in this project, please report it privately:

- **Email:** kommuniverse@gmail.com
- **Subject:** [SECURITY] Hey Jarvis Vulnerability Report

Do not create public GitHub issues for security vulnerabilities.

## Security Checklist

Before deploying or distributing:

- [ ] All API keys are in `.env` file (not hardcoded)
- [ ] `.env` file is in `.gitignore`
- [ ] `.env.example` is provided with placeholder values
- [ ] No sensitive data in Git history
- [ ] Users are informed about data processing
- [ ] Local-only models are used where possible

---

**Security is everyone's responsibility. Stay vigilant!** 🔒
