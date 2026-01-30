"""
Receiver - Reads and decrypts messages from insecure channel

Reads encrypted ciphertext from message.txt (simulating reception from an
insecure channel) and decrypts it using Caesar cipher.
"""

import sys
from caesar import decrypt, DEFAULT_SHIFT


def main():
    """
    Main receiver program - reads message.txt and decrypts content.
    
    Usage:
        python receiver.py [shift]
        python receiver.py              # Uses default shift (13)
    
    Reads the encrypted message from message.txt, strips the "v1." version
    tag, and decrypts using the provided shift value.
    """
    # Get shift value (use default if not provided)
    shift = DEFAULT_SHIFT
    if len(sys.argv) >= 2:
        try:
            shift = int(sys.argv[1])
        except ValueError:
            print(f"Error: Shift must be an integer, got '{sys.argv[1]}'")
            sys.exit(1)
    
    # Read from message.txt (insecure channel simulation)
    try:
        with open("message.txt", "r") as f:
            versioned_ciphertext = f.read().strip()
        
        if not versioned_ciphertext:
            print("Error: No message found in message.txt")
            sys.exit(1)
        
    except FileNotFoundError:
        print("Error: message.txt not found. No message to decrypt.")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading message.txt: {e}")
        sys.exit(1)
    
    # Strip version tag if present
    ciphertext = versioned_ciphertext
    if versioned_ciphertext.startswith("v1."):
        ciphertext = versioned_ciphertext[3:]  # Remove "v1." prefix
    
    # Decrypt the message
    plaintext = decrypt(ciphertext, shift)
    
    # Output the decrypted message
    print(plaintext)


if __name__ == "__main__":
    main()
