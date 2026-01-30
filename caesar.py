"""
Caesar Cipher Implementation

Educational module demonstrating classical substitution cipher with circular alphabet.
Implements encryption and decryption using modulo arithmetic for wraparound behavior.

Security Warning: Caesar cipher is NOT secure for real-world use. This is for 
educational purposes only to understand cryptographic concepts.
"""

# Default shift value - ROT13 for self-inverse property
DEFAULT_SHIFT = 13


def encrypt(plaintext: str, shift: int = DEFAULT_SHIFT) -> str:
    """
    Encrypts plaintext using Caesar cipher with circular alphabet.
    
    The Caesar cipher shifts each letter by a fixed number of positions in the
    alphabet. Uses modulo 26 arithmetic to handle wraparound (Z + 1 = A).
    
    Args:
        plaintext: Message to encrypt (will be converted to uppercase)
        shift: Number of positions to shift (default: 13 for ROT13)
               Accepts any integer - normalized via modulo 26
    
    Returns:
        Encrypted ciphertext (uppercase, non-alphabetic characters preserved)
    
    Examples:
        >>> encrypt("HELLO WORLD", 3)
        'KHOOR ZRUOG'
        >>> encrypt("HELLO WORLD", -1)
        'GDKKN VNQKC'
        >>> encrypt("HELLO WORLD", 13)
        'URYYB JBEYQ'
    """
    if not plaintext:
        return ""
    
    # Normalize shift to 0-25 range using modulo
    shift = shift % 26
    
    # Convert to uppercase for classical cipher behavior
    plaintext = plaintext.upper()
    
    result = []
    for char in plaintext:
        if char.isalpha():
            # Shift letter using circular alphabet arithmetic
            # Formula: (position + shift) mod 26
            encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            result.append(encrypted_char)
        else:
            # Preserve non-alphabetic characters (spaces, punctuation, numbers)
            result.append(char)
    
    return ''.join(result)


def decrypt(ciphertext: str, shift: int = DEFAULT_SHIFT) -> str:
    """
    Decrypts ciphertext using Caesar cipher with circular alphabet.
    
    Reverses the encryption by shifting letters backwards. Due to modulo
    arithmetic, decryption is equivalent to encryption with negative shift.
    
    Args:
        ciphertext: Encrypted message to decrypt (should be uppercase)
        shift: Number of positions used during encryption (default: 13)
               Must match the shift value used for encryption
    
    Returns:
        Decrypted plaintext (uppercase, non-alphabetic characters preserved)
    
    Examples:
        >>> decrypt("KHOOR ZRUOG", 3)
        'HELLO WORLD'
        >>> decrypt("URYYB JBEYQ", 13)
        'HELLO WORLD'
    """
    if not ciphertext:
        return ""
    
    # Decryption is encryption with negative shift
    # (-shift) % 26 handles the circular alphabet correctly
    return encrypt(ciphertext, -shift)
