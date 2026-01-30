# Crypto Messenger

Educational Python project demonstrating secure message transmission using classical Caesar cipher cryptography.

## Overview

This project simulates encrypted communication over an insecure channel (file-based message exchange). It consists of two independent programs:

- **Sender**: Encrypts plaintext messages using Caesar cipher
- **Receiver**: Decrypts ciphertext messages using the same cipher and key

The system demonstrates how encryption protects message confidentiality even when transmitted over public channels.

## Features

- ✅ Caesar cipher with ROT13 (shift 13) as smart default
- ✅ Uppercase-only classical cipher behavior
- ✅ Modulo arithmetic for any integer shift value
- ✅ Version-tagged ciphertext format (`v1.CIPHERTEXT`)
- ✅ File-based message transmission simulation
- ✅ Comprehensive test suite with 25+ unit and integration tests

## Installation

```bash
# Clone the repository
git clone https://github.com/Code-Cadet/crypto-messenger.git
cd crypto-messenger

# Install testing dependencies (optional)
pip install -r requirements.txt

# Install rich library for modern UI (optional)
pip install rich
```

## Usage

### Command-Line Interface (CLI)

#### Encrypting and Sending Messages

```bash
# Send message with custom shift
python sender.py "ATTACK AT DAWN" 13

# Send message with default shift (13)
python sender.py "HELLO WORLD"
```

The sender encrypts the message and writes it to `message.txt` with a version tag:
```
v1.URYYB JBEYQ
```

#### Receiving and Decrypting Messages

```bash
# Receive message with specific shift
python receiver.py 13

# Receive message with default shift (13)
python receiver.py
```

The receiver reads `message.txt`, strips the version tag, and outputs the decrypted plaintext:
```
HELLO WORLD
```

### Rich Terminal UI (Interactive)

For a modern, colorful terminal experience with menus and panels:

```bash
# Install rich library first
pip install rich

# Launch interactive UI
python rich_messenger.py
```

**Features:**
- 🎨 Colorful panels and tables
- 📋 Interactive menu system
- 📤 Guided encryption workflow
- 📥 Guided decryption workflow
- 📄 Message file viewer
- 🔄 ROT13 demonstration mode
- ⌨️ Smart prompts with defaults

**Rich UI Screenshots:**
- Beautiful color-coded output
- Clear section separation with borders
- Step-by-step guided workflows
- Visual feedback for all operations

## How It Works

### Caesar Cipher Algorithm

The Caesar cipher shifts each letter by a fixed number of positions in the alphabet:

```python
# Encryption formula
encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))

# Decryption formula
decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
```

**Key Features:**
- Circular alphabet: 'Z' + 1 wraps to 'A'
- Modulo normalization: Any integer shift accepted
- Non-alphabetic preservation: Spaces, punctuation, numbers unchanged

### Examples

```bash
Input:  "HELLO WORLD", Shift: 3
Output: "KHOOR ZRUOG"

Input:  "HELLO WORLD", Shift: -1
Output: "GDKKN VNQKC"

Input:  "HELLO WORLD", Shift: 13 (ROT13)
Output: "URYYB JBEYQ"
```

### Version-Tagged Format

The `v1.` prefix indicates Caesar cipher without revealing the shift value:
- Simulates real-world protocol versioning
- Separates metadata from payload
- Future-proof design (allows for `v2`, `v3` extensions)

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test class
python -m pytest tests/test_caesar.py::TestCaesarCipher -v
```

### Test Coverage

- ✅ Various shifts: 0, 1, 3, 13, 25, -1, 26, 52
- ✅ Edge cases: empty strings, spaces, mixed alphanumeric
- ✅ ROT13 self-inverse property verification
- ✅ Non-alphabetic character preservation
- ✅ Encrypt-decrypt roundtrip validation
- ✅ Version tag handling
- ✅ End-to-end sender-receiver integration

## Project Structure

```
crypto-messenger/
├── .github/
│   └── copilot-instructions.md    # AI agent guidance
├── sender.py                      # Encryption program
├── receiver.py                    # Decryption program
├── caesar.py                      # Caesar cipher implementation
├── message.txt                    # Transmission channel (git-ignored)
├── tests/
│   └── test_caesar.py             # Unit and integration tests
├── requirements.txt               # Testing dependencies
├── .gitignore                     # Git exclusions
└── README.md                      # This file
```

## Educational Context

### Why Caesar Cipher?

The Caesar cipher (named after Julius Caesar) is one of the oldest and simplest encryption techniques:
- **Historical significance**: Used by Julius Caesar for military communications
- **Educational value**: Clear demonstration of substitution ciphers and modulo arithmetic
- **Self-inverse property** (ROT13): Encryption and decryption use the same operation

### Security Warning

⚠️ **Caesar cipher is NOT secure for real-world use:**
- Only 26 possible keys (trivial brute force attack)
- Vulnerable to frequency analysis
- No protection against modern cryptanalysis
- **Use for learning cryptographic concepts only**

For real-world security, use established cryptographic libraries like:
- Python: `cryptography`, `PyCryptodome`
- Industry standards: AES, RSA, ChaCha20

## Development Workflow

### Command-Line Usage

#### Typical Message Exchange

```bash
# Step 1: Alice encrypts and sends
python sender.py "MEET AT MIDNIGHT" 7
# Writes to message.txt: v1.TLLA HA TPKUPNOM

# Step 2: Message intercepted (readable but meaningless without key)
cat message.txt
# v1.TLLA HA TPKUPNOM

# Step 3: Bob receives and decrypts
python receiver.py 7
# MEET AT MIDNIGHT
```

#### Smart Defaults in Action

```bash
# Both sender and receiver use DEFAULT_SHIFT = 13
python sender.py "SECRET MESSAGE"
python receiver.py
# Output: SECRET MESSAGE
```

### Rich Terminal UI Usage

Launch the interactive menu system for a guided experience:

```bash
python rich_messenger.py
```

**Menu Options:**
1. **📤 Encrypt Message** - Enter message and shift interactively
2. **📥 Decrypt Message** - Load from `message.txt` and decrypt
3. **📄 View Message File** - Inspect current encrypted message
4. **🔄 ROT13 Demo** - See self-inverse property in action
5. **❌ Exit** - Close the application

The Rich UI provides:
- Visual feedback with colored panels
- Input validation and helpful error messages
- Default values (press Enter for ROT13)
- Clear workflow guidance

## Why ROT13?

ROT13 (shift 13) is special because:
1. **Self-inverse**: `encrypt(encrypt(text, 13), 13) == text`
2. **Symmetric**: Same operation for encryption and decryption
3. **Well-known**: Historically used for spoiler protection in forums

## Contributing

This is an educational project. Contributions welcome for:
- Additional test cases
- Documentation improvements
- Code clarity enhancements
- Educational explanations

## License

MIT License - Free for educational use

## Author

Created for cryptography education and coursework demonstration.

---

**Remember**: This demonstrates cryptographic concepts. Never use classical ciphers for real security needs!
