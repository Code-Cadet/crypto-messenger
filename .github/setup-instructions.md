# Copilot Instructions for crypto-messenger

## Project Overview
Educational Python project demonstrating secure message transmission using Caesar cipher. Simulates encrypted communication over an insecure channel (file-based message exchange). Focus on clarity, correctness, and conceptual demonstration—not production cryptographic security.

## Architecture

### Core Modules
- `sender.py` - Encrypts plaintext messages and writes to `message.txt`
- `receiver.py` - Reads and decrypts ciphertext from `message.txt`
- `caesar.py` - Shared Caesar cipher implementation (encrypt/decrypt functions)
- `message.txt` - Simulates insecure transmission channel (contains only ciphertext)

### Design Principles
- **Separation of concerns**: Distinct sender/receiver programs sharing cipher logic
- **Smart defaults**: Use `DEFAULT_SHIFT = 13` (ROT13) when shift omitted
- **Robust internals, minimalist output**: Handle edge cases gracefully, show clean results
- **Version-tagged format**: Prefix ciphertext with `v1.` to indicate Caesar cipher without revealing shift

## Command-Line Interface

```bash
# Sender usage
python sender.py "ATTACK AT DAWN" 13    # Custom shift
python sender.py "ATTACK AT DAWN"       # Uses default shift (13)

# Receiver usage
python receiver.py 13                   # Reads message.txt, decrypts with shift 13
python receiver.py                      # Uses default shift (13)
```

## Caesar Cipher Implementation

### Core Algorithm
```python
# Encryption/Decryption formula (letters only)
encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
```

### Key Rules
- **Uppercase only**: Convert all input to uppercase for classical accuracy
- **Modulo normalization**: Accept any integer shift, normalize via `% 26`
- **Preserve non-alphabetic**: Spaces, punctuation, numbers pass through unchanged
- **Circular alphabet**: 'Z' + 1 = 'A' (wraparound behavior)

### Examples
```
Input: "HELLO WORLD", Shift: 3  → Output: "KHOOR ZRUOG"
Input: "HELLO WORLD", Shift: -1 → Output: "GDKKN VNQKC" (equivalent to shift 25)
Input: "HELLO WORLD", Shift: 13 → Output: "URYYB JBEYQ" (ROT13)
```

## Version-Tagged Output Format

### Purpose
Indicates cipher type without revealing the shift value (simulates real-world protocol versioning).

### Format
```
v1.CIPHERTEXT
```

Example:
```
# sender.py outputs to message.txt
v1.URYYB JBEYQ

# receiver.py reads, strips "v1.", decrypts
HELLO WORLD
```

### Implementation
- Sender: Prepend `v1.` before writing to `message.txt`
- Receiver: Detect and strip `v1.` prefix before decryption
- `v1` = Caesar cipher (future versions could indicate other ciphers if extended)

## File-Based Communication Flow

1. **Sender encrypts**: Reads plaintext from command-line arg → encrypts with Caesar → writes `v1.CIPHERTEXT` to `message.txt`
2. **Insecure channel**: `message.txt` represents intercepted message (readable by anyone, but meaningless without key)
3. **Receiver decrypts**: Reads `message.txt` → strips version tag → decrypts with same shift → displays plaintext

## Python Conventions

### Code Style
- Follow PEP 8 naming and formatting
- Use type hints: `def encrypt(plaintext: str, shift: int) -> str:`
- Comprehensive docstrings explaining cryptographic concepts
- Constants in UPPER_CASE: `DEFAULT_SHIFT = 13`

### Error Handling
- **Robust internal validation**: Check for None, empty strings, invalid types
- **Smart defaults**: Missing shift → use `DEFAULT_SHIFT = 13`
- **Minimal user-facing errors**: Fix what you can (strip whitespace, handle case), fail clearly when you can't
- Informative messages: "No message provided" rather than generic exceptions

### Example Structure
```python
# caesar.py
DEFAULT_SHIFT = 13

def encrypt(plaintext: str, shift: int = DEFAULT_SHIFT) -> str:
    """
    Encrypts plaintext using Caesar cipher with circular alphabet.
    
    Args:
        plaintext: Message to encrypt (converted to uppercase)
        shift: Number of positions to shift (default: 13 for ROT13)
    
    Returns:
        Encrypted ciphertext (uppercase, non-alpha preserved)
    """
    # Implementation with modulo arithmetic
```

## Testing Strategy

### Unit Tests (`tests/test_caesar.py`)
- Test various shifts: 0, 1, 13, 25, -1, 26, 52 (verify modulo normalization)
- Test edge cases: empty string, all spaces, mixed alphanumeric
- Test ROT13 self-inverse property: `encrypt(encrypt(text, 13), 13) == text`
- Test non-alphabetic preservation: punctuation, numbers unchanged

### Integration Tests
- End-to-end: Encrypt with sender → write file → read file → decrypt with receiver
- Version tag handling: Verify `v1.` prefix added/stripped correctly
- Default shift behavior: Test omitting shift argument uses 13

### Run Tests
```bash
python -m pytest tests/
```

## Key Implementation Notes

### Why ROT13 (Shift 13)?
- Self-inverse property: Encryption and decryption use same operation
- Educational value: Demonstrates symmetric cipher simplicity
- Historical significance: Widely known classical cipher variant

### Why Uppercase Only?
- Historical accuracy: Classical ciphers used capital letters
- Simplifies implementation: Single case to handle
- Clear output: Ciphertext visually distinct from plaintext

### Why Version Tags?
- Simulates real protocol design: Version metadata separate from payload
- Educational concept: Shows how systems indicate cipher type without exposing keys
- Future-proof marker: `v1` implies room for `v2`, `v3` (even if not implemented)

### Security Context (Educational Warning)
⚠️ **Caesar cipher is NOT secure for real-world use**:
- Only 26 possible keys (trivial brute force)
- Vulnerable to frequency analysis
- No protection against modern cryptanalysis
- Use this for learning cryptographic concepts only

## Expected Project Structure
```
crypto-messenger/
├── .github/
│   └── copilot-instructions.md
├── sender.py           # Encryption program
├── receiver.py         # Decryption program
├── caesar.py           # Shared cipher logic
├── message.txt         # Transmission channel (git-ignored)
├── tests/
│   └── test_caesar.py  # Unit and integration tests
├── requirements.txt    # Dependencies (pytest for testing)
└── README.md           # User-facing documentation
```

## Development Workflow

### Typical Usage
```bash
# 1. Send encrypted message
python sender.py "ATTACK AT DAWN" 13
# Writes to message.txt: v1.NGGNPX NG QNJA

# 2. Simulate message interception
# (message.txt represents insecure channel - readable but encrypted)

# 3. Receive and decrypt
python receiver.py 13
# Reads message.txt, outputs: ATTACK AT DAWN
```

### Smart Default Example
```bash
# Both use DEFAULT_SHIFT = 13
python sender.py "SECRET MESSAGE"
python receiver.py
# Output: SECRET MESSAGE
```
