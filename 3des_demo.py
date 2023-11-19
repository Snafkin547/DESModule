# Triple-DES Encryption

from utils import *
from tables import *
from des import DES


# Generate 64 bits input
input_size = 64
input_val, input_bits = generate_bit(input_size)

# Generate 64 bits input
orig_key_size = 64
key0, key_bits0 = generate_bit(orig_key_size)
key1, key_bits1 = generate_bit(orig_key_size)
key2, key_bits2 = generate_bit(orig_key_size)

# Initiate DES
DES_inst = DES()

# Triple-DES encryption
enc_val, enc_bits = DES_inst.encrypt(input_bits, key_bits0)
dec_val, dec_bits = DES_inst.decrypt(enc_bits, key_bits1)
final_val, final_bits = DES_inst.encrypt(dec_bits, key_bits2)

# Triple-DES decryption
rdec_val, rdec_bits = DES_inst.decrypt(final_bits, key_bits2)
renc_val, renc_bits = DES_inst.encrypt(rdec_bits, key_bits1)
rfinal_val, rfinal_bits = DES_inst.decrypt(renc_bits, key_bits0)

# Result and proof of symmetricity
print(f"\ninput value     :{input_val}")
print(f"decrypted value :{rfinal_val}")
assert rfinal_val == input_val
