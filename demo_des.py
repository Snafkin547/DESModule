from src import *


key = 8289481480542705629

# Generate 64 bits input
input_size = 64
# input_val, input_bits = generate_bit(input_size)
input_val = 3271167758276528483

# fmt: off
input_bits = [0, 0, 1, 0, 1, 1, 0, 1, 
          0, 1, 1, 0, 0, 1, 0, 1, 
          1, 0, 0, 0, 0, 1, 0, 1, 
          1, 0, 1, 1, 1, 1, 1, 0, 
          1, 0, 1, 0, 1, 0, 0, 0, 
          1, 1, 0, 0, 1, 0, 0, 0, 
          1, 0, 0, 0, 1, 0, 0, 1, 
          0, 1, 1, 0, 0, 0, 1, 1]

assert len(input_bits) == input_size
# fmt: on

# Initiate DES
DES_inst = DES(key)


# DES encryption
enc_val, enc_bits = DES_inst.encrypt(input_bits)
assert len(enc_bits) == 64
print(f"\nencrypted value :{enc_val}")


# DES decryption
dec_val, dec_bits = DES_inst.decrypt(enc_bits)
print(f"\ninput value     :{input_val}")
print(f"decrypted value :{dec_val}")
assert input_val == dec_val
