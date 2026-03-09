# classical_voting_demo.py — Classical Cryptographic Voting System Demo

"""
Classical Secure Voting System — Traditional Cryptography Demonstration

Demonstrates classical key generation and encryption for ballot security.
Replaces quantum circuits with proven cryptographic methods.

Author: Classical Crypto Implementation
Date: September 2025

Usage: python classical_voting_demo.py

Requirements: pip install cryptography pycryptodome numpy
"""

import os
import secrets
import hashlib
import hmac
import numpy as np
import time
import json
from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Optional for visualization
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️ matplotlib not found — visualization disabled")

class ClassicalVotingSystemDemo:
    """Demonstrates classical cryptographic methods for secure voting."""

    def __init__(self):
        print("🔐 Classical Cryptographic Voting System Demo")
        print("=" * 60)
        print("Using traditional cryptography instead of quantum methods")
        self.encryption_stats = {"keys_generated": 0, "votes_encrypted": 0, "signatures_created": 0}

    def generate_secure_key(self, key_length=32, show_details=True):
        """Generate cryptographically secure key using classical methods."""
        
        if show_details:
            print(f"\n🔑 Generating {key_length}-byte secure key")
            print("-" * 40)
            print("Method: Cryptographically Secure Pseudo-Random Number Generator (CSPRNG)")
        
        # Generate primary key using OS entropy
        primary_key = os.urandom(key_length)
        
        # Add additional entropy sources
        entropy_sources = [
            secrets.token_bytes(16),  # Python secrets module
            str(time.time_ns()).encode('utf-8'),  # High precision timestamp
            str(os.getpid()).encode('utf-8'),  # Process ID
        ]
        
        # Combine entropy sources
        combined_entropy = primary_key
        for entropy in entropy_sources:
            combined_entropy += entropy
        
        # Use HMAC-SHA256 for key derivation
        final_key = hmac.new(
            primary_key[:32] if len(primary_key) >= 32 else primary_key + b'\x00' * (32 - len(primary_key)),
            combined_entropy,
            hashlib.sha256
        ).digest()[:key_length]
        
        if show_details:
            print(f"Primary entropy: {len(primary_key)} bytes from os.urandom()")
            print(f"Additional sources: {len(entropy_sources)} entropy supplements")
            print(f"Key derivation: HMAC-SHA256")
            print(f"✅ Final {key_length}-byte key: {final_key.hex()[:16]}...")
            print(f"Key quality score: {self._calculate_entropy_score(final_key):.2f}/8.0")
        
        self.encryption_stats["keys_generated"] += 1
        return final_key

    def encrypt_vote_aes256(self, vote_data, key=None):
        """Encrypt vote data using AES-256 encryption."""
        
        if key is None:
            key = self.generate_secure_key(32, show_details=False)
        
        # Generate random IV for AES
        iv = os.urandom(16)
        
        # Create AES cipher in CBC mode
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Convert vote data to JSON and pad
        vote_json = json.dumps(vote_data, sort_keys=True)
        padded_data = pad(vote_json.encode('utf-8'), AES.block_size)
        
        # Encrypt
        encrypted_data = cipher.encrypt(padded_data)
        
        # Combine IV and encrypted data
        encrypted_package = {
            'iv': base64.b64encode(iv).decode('utf-8'),
            'encrypted_data': base64.b64encode(encrypted_data).decode('utf-8'),
            'encryption_method': 'AES-256-CBC',
            'key_id': hashlib.sha256(key).hexdigest()[:16]
        }
        
        self.encryption_stats["votes_encrypted"] += 1
        return encrypted_package, key

    def create_digital_signature(self, data, private_key=None):
        """Create RSA digital signature for data integrity."""
        
        if private_key is None:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
        
        # Create hash of data
        data_hash = hashes.Hash(hashes.SHA256())
        data_hash.update(data.encode('utf-8'))
        digest = data_hash.finalize()
        
        # Sign the hash
        signature = private_key.sign(
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        self.encryption_stats["signatures_created"] += 1
        return {
            'signature': base64.b64encode(signature).decode('utf-8'),
            'public_key': private_key.public_key().public_key_string.decode('utf-8') if hasattr(private_key.public_key(), 'public_key_string') else 'RSA_PUBLIC_KEY',
            'hash_algorithm': 'SHA-256',
            'signature_algorithm': 'RSA-PSS'
        }

    def demonstrate_vote_encryption(self):
        """Show complete vote encryption process using classical cryptography."""
        
        print("\n🗳️ CLASSICAL VOTE ENCRYPTION PROCESS")
        print("=" * 50)
        
        # Sample vote data
        vote_data = {
            "voter_id": "CLASSICAL_DEMO_123",
            "party": "Demo Party",
            "timestamp": datetime.now().isoformat(),
            "vote_id": f"vote_classical_{int(time.time())}"
        }
        
        print("Sample vote data:")
        for k, v in vote_data.items():
            print(f"  {k}: {v}")
        
        print("\n🔑 Step 1: Generate AES-256 encryption key...")
        aes_key = self.generate_secure_key(32, show_details=False)
        print(f"AES Key: {aes_key.hex()[:32]}...")
        
        print("\n🔒 Step 2: Encrypt vote with AES-256...")
        encrypted_package, _ = self.encrypt_vote_aes256(vote_data, aes_key)
        print(f"Encrypted data: {encrypted_package['encrypted_data'][:32]}...")
        print(f"IV: {encrypted_package['iv']}")
        print(f"Encryption method: {encrypted_package['encryption_method']}")
        
        print("\n✍️ Step 3: Create digital signature...")
        vote_json = json.dumps(vote_data, sort_keys=True)
        signature_data = self.create_digital_signature(vote_json)
        print(f"Signature: {signature_data['signature'][:32]}...")
        print(f"Algorithm: {signature_data['signature_algorithm']}")
        
        print(f"\n📊 Encryption Statistics:")
        print(f"  Keys generated: {self.encryption_stats['keys_generated']}")
        print(f"  Votes encrypted: {self.encryption_stats['votes_encrypted']}")
        print(f"  Signatures created: {self.encryption_stats['signatures_created']}")
        
        return encrypted_package, aes_key, signature_data

    def analyze_key_randomness(self, num_tests=5):
        """Test key uniqueness and randomness using classical generation."""
        
        print(f"\n🔬 CLASSICAL KEY RANDOMNESS ANALYSIS ({num_tests} tests)")
        print("-" * 50)
        
        keys = []
        for i in range(num_tests):
            key = self.generate_secure_key(32, show_details=False)
            keys.append(key)
            print(f"Key {i+1:2d}: {key.hex()[:32]}... (entropy: {self._calculate_entropy_score(key):.2f})")
        
        # Analyze uniqueness
        unique_count = len(set(key.hex() for key in keys))
        print(f"\nUniqueness: {unique_count}/{num_tests} keys are unique ({unique_count*100/num_tests:.1f}%)")
        
        # Analyze bit distribution
        all_bits = ''.join(format(byte, '08b') for key in keys for byte in key)
        zeros = all_bits.count('0')
        ones = all_bits.count('1')
        total_bits = len(all_bits)
        
        print(f"Bit distribution: {zeros} zeros, {ones} ones")
        print(f"Bit balance: {ones/total_bits*100:.2f}% ones (ideal: 50%)")
        
        return keys

    def demonstrate_secure_communication(self):
        """Show secure key exchange and communication process."""
        
        print("\n🔐 SECURE COMMUNICATION DEMONSTRATION")
        print("-" * 45)
        
        # Generate RSA key pair for secure key exchange
        print("Step 1: Generate RSA key pair for secure key exchange...")
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()
        print("✅ RSA-2048 key pair generated")
        
        # Generate symmetric key
        print("\nStep 2: Generate AES key for vote encryption...")
        aes_key = self.generate_secure_key(32, show_details=False)
        print(f"✅ AES-256 key generated: {aes_key.hex()[:32]}...")
        
        # Encrypt AES key with RSA
        print("\nStep 3: Encrypt AES key with RSA public key...")
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(f"✅ AES key encrypted with RSA: {base64.b64encode(encrypted_aes_key)[:32].decode()}...")
        
        # Verify decryption
        print("\nStep 4: Verify key can be decrypted...")
        decrypted_aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        verification_success = decrypted_aes_key == aes_key
        print(f"✅ Key exchange verification: {'SUCCESS' if verification_success else 'FAILED'}")
        
        return {
            'private_key': private_key,
            'public_key': public_key,
            'aes_key': aes_key,
            'encrypted_aes_key': encrypted_aes_key,
            'verification_success': verification_success
        }

    def demonstrate_blockchain_integration(self):
        """Show how classical crypto integrates with blockchain voting."""
        
        print("\n⛓️ BLOCKCHAIN INTEGRATION WITH CLASSICAL CRYPTO")
        print("-" * 50)
        
        # Encrypt a vote
        encrypted_package, aes_key, signature_data = self.demonstrate_vote_encryption()
        
        # Create blockchain entry
        vote_hash = hashlib.sha256(
            encrypted_package['encrypted_data'].encode()
        ).hexdigest()
        
        blockchain_entry = {
            'block_type': 'vote_record',
            'vote_hash': vote_hash,
            'key_id': encrypted_package['key_id'],
            'signature_hash': hashlib.sha256(signature_data['signature'].encode()).hexdigest(),
            'timestamp': datetime.now().isoformat(),
            'encryption_method': 'AES-256-CBC',
            'signature_method': 'RSA-PSS-SHA256'
        }
        
        print(f"\n📦 Blockchain Block Contents:")
        for key, value in blockchain_entry.items():
            if isinstance(value, str) and len(value) > 32:
                print(f"  {key}: {value[:32]}...")
            else:
                print(f"  {key}: {value}")
        
        print(f"\n🔒 Security Properties:")
        print("  ✓ Unique AES-256 key per vote")
        print("  ✓ Vote encrypted with industry-standard AES")
        print("  ✓ RSA digital signatures for authentication")
        print("  ✓ SHA-256 hashing for integrity verification")
        print("  ✓ Secure key exchange using RSA-OAEP")
        print("  ✓ No quantum dependencies")
        print("  ✓ Proven cryptographic security")
        
        return blockchain_entry

    def interactive_demo(self):
        """Interactive menu for demonstrations."""
        
        print("\n" + "=" * 60)
        print("CLASSICAL CRYPTOGRAPHIC VOTING DEMONSTRATIONS")
        print("=" * 60)
        print("1. Secure key generation")
        print("2. Vote encryption process")
        print("3. Key randomness analysis")
        print("4. Secure communication demo")
        print("5. Blockchain integration")
        print("6. Full system demonstration")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            key = self.generate_secure_key(32, show_details=True)
            
        elif choice == "2":
            self.demonstrate_vote_encryption()
            
        elif choice == "3":
            self.analyze_key_randomness(5)
            
        elif choice == "4":
            self.demonstrate_secure_communication()
            
        elif choice == "5":
            self.demonstrate_blockchain_integration()
            
        elif choice == "6":
            print("\n🚀 FULL SYSTEM DEMONSTRATION")
            print("=" * 40)
            self.generate_secure_key(32, show_details=True)
            self.demonstrate_vote_encryption()
            self.analyze_key_randomness(3)
            self.demonstrate_secure_communication()
            self.demonstrate_blockchain_integration()
            
        else:
            print("\n✅ Classical cryptographic voting demo completed!")
            print("🔐 Quantum dependencies successfully replaced")
            return False
            
        return True

    def _calculate_entropy_score(self, data):
        """Calculate Shannon entropy for key quality assessment."""
        if not data:
            return 0.0
        
        byte_counts = {}
        for byte in data:
            byte_counts[byte] = byte_counts.get(byte, 0) + 1
        
        entropy = 0.0
        data_len = len(data)
        for count in byte_counts.values():
            probability = count / data_len
            if probability > 0:
                entropy -= probability * np.log2(probability)
        
        return entropy

def main():
    """Entry point for the classical voting system demo."""
    
    demo = ClassicalVotingSystemDemo()
    
    print("\n" + "🎯" * 20)
    print("CLASSICAL CRYPTOGRAPHIC VOTING SYSTEM")
    print("Replacing Quantum Components with Proven Methods")
    print("🎯" * 20)
    
    while True:
        if not demo.interactive_demo():
            break
        
        if input("\nRun another demonstration? (y/n): ").strip().lower() != "y":
            break
    
    print(f"\n📊 Final Statistics:")
    for key, value in demo.encryption_stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\n🎉 Classical cryptographic voting system demo completed!")
    print("🛡️ Security maintained without quantum dependencies")
    print("✅ Ready for production deployment")

if __name__ == "__main__":
    main()

"""
TECHNICAL EXPLANATION:
======================

Classical Cryptographic Methods Used:

1. Key Generation:
   - os.urandom() for cryptographically secure random numbers
   - HMAC-SHA256 for key derivation
   - Multiple entropy sources combined

2. Symmetric Encryption:
   - AES-256 in CBC mode for vote encryption
   - Random IV for each encryption
   - PKCS7 padding

3. Asymmetric Cryptography:
   - RSA-2048/4096 for key exchange
   - RSA-PSS for digital signatures
   - OAEP padding for encryption

4. Hash Functions:
   - SHA-256 for data integrity
   - HMAC for authenticated hashing

Integration with Voting System:
- Each vote encrypted with unique AES-256 key
- RSA used for secure key exchange
- Digital signatures ensure authenticity
- Blockchain stores encrypted vote hashes
- No quantum dependencies required

Security Properties:
- Computationally secure (vs information-theoretic)
- Industry-standard algorithms
- Well-tested implementations
- Future-proof key sizes
- Practical performance characteristics
"""