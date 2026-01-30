"""
Unit and Integration Tests for Caesar Cipher Messenger

Tests the encryption/decryption logic and end-to-end message transmission.
"""

import pytest
import os
from caesar import encrypt, decrypt, DEFAULT_SHIFT


class TestCaesarCipher:
    """Unit tests for Caesar cipher encryption and decryption."""
    
    def test_encrypt_basic(self):
        """Test basic encryption with shift 3."""
        assert encrypt("HELLO WORLD", 3) == "KHOOR ZRUOG"
    
    def test_encrypt_rot13(self):
        """Test ROT13 encryption (default shift)."""
        assert encrypt("HELLO WORLD", 13) == "URYYB JBEYQ"
        assert encrypt("HELLO WORLD") == "URYYB JBEYQ"  # Default shift
    
    def test_encrypt_negative_shift(self):
        """Test encryption with negative shift."""
        assert encrypt("HELLO WORLD", -1) == "GDKKN VNQKC"
    
    def test_encrypt_shift_zero(self):
        """Test encryption with shift 0 (no change)."""
        assert encrypt("HELLO WORLD", 0) == "HELLO WORLD"
    
    def test_encrypt_shift_26(self):
        """Test encryption with shift 26 (full rotation, no change)."""
        assert encrypt("HELLO WORLD", 26) == "HELLO WORLD"
    
    def test_encrypt_large_shift(self):
        """Test encryption with large shift (modulo normalization)."""
        # Shift 52 = 26 * 2, should be same as shift 0
        assert encrypt("HELLO WORLD", 52) == "HELLO WORLD"
        # Shift 29 = 26 + 3, should be same as shift 3
        assert encrypt("HELLO WORLD", 29) == "KHOOR ZRUOG"
    
    def test_encrypt_preserves_non_alpha(self):
        """Test that non-alphabetic characters are preserved."""
        assert encrypt("HELLO, WORLD! 123", 3) == "KHOOR, ZRUOG! 123"
        assert encrypt("TEST@#$%", 5) == "YJXY@#$%"
    
    def test_encrypt_empty_string(self):
        """Test encryption of empty string."""
        assert encrypt("", 3) == ""
    
    def test_encrypt_only_spaces(self):
        """Test encryption of string with only spaces."""
        assert encrypt("   ", 3) == "   "
    
    def test_encrypt_lowercase_converted(self):
        """Test that lowercase input is converted to uppercase."""
        assert encrypt("hello world", 3) == "KHOOR ZRUOG"
        assert encrypt("HeLLo WoRLd", 3) == "KHOOR ZRUOG"
    
    def test_decrypt_basic(self):
        """Test basic decryption with shift 3."""
        assert decrypt("KHOOR ZRUOG", 3) == "HELLO WORLD"
    
    def test_decrypt_rot13(self):
        """Test ROT13 decryption."""
        assert decrypt("URYYB JBEYQ", 13) == "HELLO WORLD"
        assert decrypt("URYYB JBEYQ") == "HELLO WORLD"  # Default shift
    
    def test_decrypt_negative_shift(self):
        """Test decryption with negative shift."""
        assert decrypt("GDKKN VNQKC", -1) == "HELLO WORLD"
    
    def test_decrypt_preserves_non_alpha(self):
        """Test that decryption preserves non-alphabetic characters."""
        assert decrypt("KHOOR, ZRUOG! 123", 3) == "HELLO, WORLD! 123"
    
    def test_rot13_self_inverse(self):
        """Test ROT13 self-inverse property: encrypt(encrypt(x)) = x."""
        text = "HELLO WORLD"
        encrypted_once = encrypt(text, 13)
        encrypted_twice = encrypt(encrypted_once, 13)
        assert encrypted_twice == text
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test that decrypt(encrypt(text)) = text."""
        original = "ATTACK AT DAWN"
        for shift in [1, 3, 7, 13, 25]:
            encrypted = encrypt(original, shift)
            decrypted = decrypt(encrypted, shift)
            assert decrypted == original, f"Roundtrip failed for shift {shift}"
    
    def test_encrypt_decrypt_with_special_chars(self):
        """Test roundtrip with special characters."""
        original = "HELLO, WORLD! HOW ARE YOU? 123"
        encrypted = encrypt(original, 5)
        decrypted = decrypt(encrypted, 5)
        assert decrypted == original
    
    def test_alphabet_wraparound(self):
        """Test circular alphabet behavior at boundaries."""
        assert encrypt("XYZ", 3) == "ABC"  # X+3=A, Y+3=B, Z+3=C
        assert encrypt("ABC", -3) == "XYZ"  # A-3=X, B-3=Y, C-3=Z
        assert decrypt("ABC", 3) == "XYZ"  # Decrypt reverses


class TestIntegration:
    """Integration tests for end-to-end message transmission."""
    
    def setup_method(self):
        """Clean up message.txt before each test."""
        if os.path.exists("message.txt"):
            os.remove("message.txt")
    
    def teardown_method(self):
        """Clean up message.txt after each test."""
        if os.path.exists("message.txt"):
            os.remove("message.txt")
    
    def test_sender_receiver_integration(self):
        """Test complete sender-receiver flow with file I/O."""
        import sender
        import receiver
        import sys
        from io import StringIO
        
        # Simulate sender
        original_message = "ATTACK AT DAWN"
        shift_value = 13
        
        sys.argv = ["sender.py", original_message, str(shift_value)]
        
        # Capture output
        captured_output = StringIO()
        sys.stdout = captured_output
        
        sender.main()
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        # Verify message.txt exists and has version tag
        assert os.path.exists("message.txt")
        with open("message.txt", "r") as f:
            content = f.read()
        assert content.startswith("v1.")
        
        # Simulate receiver
        sys.argv = ["receiver.py", str(shift_value)]
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        receiver.main()
        
        sys.stdout = sys.__stdout__
        
        # Check decrypted output
        output = captured_output.getvalue().strip()
        assert output == original_message
    
    def test_version_tag_handling(self):
        """Test that version tag is correctly added and stripped."""
        # Write a message with version tag
        with open("message.txt", "w") as f:
            f.write("v1.URYYB JBEYQ")
        
        import receiver
        import sys
        from io import StringIO
        
        sys.argv = ["receiver.py", "13"]
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        receiver.main()
        
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        assert output == "HELLO WORLD"
    
    def test_default_shift_integration(self):
        """Test sender and receiver using default shift."""
        import sender
        import receiver
        import sys
        from io import StringIO
        
        # Send with default shift
        sys.argv = ["sender.py", "SECRET MESSAGE"]
        captured = StringIO()
        sys.stdout = captured
        sender.main()
        sys.stdout = sys.__stdout__
        
        # Receive with default shift
        sys.argv = ["receiver.py"]
        captured = StringIO()
        sys.stdout = captured
        receiver.main()
        sys.stdout = sys.__stdout__
        
        output = captured.getvalue().strip()
        assert output == "SECRET MESSAGE"
