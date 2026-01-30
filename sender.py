"""
Sender - Encrypts messages and transmits via insecure channel

Encrypts plaintext messages using Caesar cipher and writes the encrypted
ciphertext to message.txt (simulating transmission over an insecure channel).
"""

import sys
from caesar import encrypt, DEFAULT_SHIFT


def main():
    """
    Main sender program - encrypts message and writes to message.txt.
    
    Usage:
        python sender.py "MESSAGE" [shift]
        python sender.py "MESSAGE"           # Uses default shift (13)
    
    The encrypted message is prefixed with "v1." to indicate Caesar cipher
    version without revealing the shift value.
    """
    # Check if message provided
    if len(sys.argv) < 2:
        print("Usage: python sender.py \"MESSAGE\" [shift]")
        print("Example: python sender.py \"ATTACK AT DAWN\" 13")
        sys.exit(1)
    
    # Get plaintext message from command-line argument
    plaintext = sys.argv[1]
    
    if not plaintext or not plaintext.strip():
        print("Error: No message provided")
        sys.exit(1)
    
    # Get shift value (use default if not provided)
    shift = DEFAULT_SHIFT
    if len(sys.argv) >= 3:
        try:
            shift = int(sys.argv[2])
        except ValueError:
            print(f"Error: Shift must be an integer, got '{sys.argv[2]}'")
            sys.exit(1)
    
    # Encrypt the message
    ciphertext = encrypt(plaintext, shift)
    
    # Add version tag to indicate cipher type (without revealing shift)
    versioned_ciphertext = f"v1.{ciphertext}"
    
    # Write to message.txt (insecure channel simulation)
    try:
        with open("message.txt", "w") as f:
            f.write(versioned_ciphertext)
        
        print(f"Message encrypted and sent to message.txt")
        print(f"Ciphertext: {versioned_ciphertext}")
        
    except IOError as e:
        print(f"Error writing to message.txt: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
