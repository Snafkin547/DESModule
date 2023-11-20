# Triple-DES Encryption

from src import *

# Generate 64 bits input
input_size = 64
input_val, input_bits = generate_bit(input_size)

# Generate 64 bits input
keys = [8289481480542705629, 8289481480542225629, 9128814805426305629]

# Initiate DES
DES_inst = triple_DES(keys)

# Triple-DES encryption
enc_val, enc_bits = DES_inst.encrypt(input_bits)

# Triple-DES decryption
final_val, final_bits = DES_inst.decrypt(enc_bits)

# Result and proof of symmetricity
print(f"\ninput value     :{input_val}")
print(f"decrypted value :{final_val}")
assert final_val == input_val
