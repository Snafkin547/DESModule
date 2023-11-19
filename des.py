from tables import *
from utils import *


# ref: https://csrc.nist.gov/files/pubs/fips/46-3/final/docs/fips46-3.pdf
class DES:
    def __init__(self):
        self.key_schedule = None

    # Key expansion from 64 bits key to n_keys sets of 48 bits key
    def key_expansion(self, key_bits):
        try:
            # Replace 'key_bits' with your actual key bits list variable
            assert len(key_bits) == 64, "Key must be 64 bits long"
            assert all(elem in [0, 1] for elem in key_bits), "All elements must be 0 or 1"
        except AssertionError as error:
            raise ValueError(str(error))

        res = []

        # Permuted choice 1
        c_key = [key_bits[x - 1] for x in pc_1_c]
        d_key = [key_bits[x - 1] for x in pc_1_d]

        for i in range(16):
            curr_shift = left_shift_schedule[i + 1]
            c_key = c_key[curr_shift:] + c_key[:curr_shift]
            d_key = d_key[curr_shift:] + d_key[:curr_shift]
            concat_key = c_key + d_key
            generated_key = [concat_key[x - 1] for x in pc_2_perm_table]
            assert len(generated_key) == 48
            res.append(generated_key)
        assert len(res) == 16
        return res

    def permutate(self, input_bits, perm_table):
        return [input_bits[x - 1] for x in perm_table]

    def s_boxify(self, split_xored_r):
        sboxed = []
        for i in range(len(split_xored_r)):
            s_input = split_xored_r[i]
            outer = int(str(s_input[0]) + str(s_input[-1]), 2)
            middle = int(str(s_input[1]) + str(s_input[2]) + str(s_input[3]) + str(s_input[4]), 2)
            s_val = sbox[i][outer][middle]
            res = int_to_bitlist(s_val, 4)
            sboxed += res
        return sboxed

    def feistel_net(self, input_bits, decrypt=False):
        for it in range(16):
            ## Half 64 bits into 2 sets of 32 bits (x and y)
            left = input_bits[0:32]
            right = input_bits[32:]
            assert len(left) == 32 and len(right) == 32

            ## E: Expand y from 32 to 48
            expanded_r = self.permutate(right, e_bit_select_table)
            assert len(expanded_r) == 48

            # Ensure the key schedule is reversed in decryption
            if decrypt == False:
                sub_key = self.key_schedule[it]
            else:
                sub_key = self.key_schedule[15 - it]

            ## XOR with 48 bits Key
            xored_r = xor(expanded_r, sub_key)
            assert len(xored_r) == 48

            ## Split the 48 bits into 8 sets (6 bits each)
            split_xored_r = [xored_r[i : i + 6] for i in range(0, 48, 6)]
            assert len(split_xored_r) == 8
            assert xored_r == [item for sublist in split_xored_r for item in sublist]

            ## S-Box: Look up table to shrink 6 bits to 4 bits
            sboxed = self.s_boxify(split_xored_r)
            assert len(sboxed) == 32

            # P: Permutate outputs (8 stes of 4 bits)
            permed_sboxed = self.permutate(sboxed, p_box_perm_table)
            assert len(permed_sboxed) == 32

            ## XOR modified right and left
            _left = xor(permed_sboxed, left)

            ## Swap left & right (if not in the last round) to re-form 64 bits
            if it != 15:
                input_bits = right + _left
            else:
                input_bits = _left + right

            assert len(input_bits) == 64

        return input_bits

    def encrypt(self, input_bits, key_bits):
        try:
            assert len(key_bits) == 64, "Key must be 64 bits long"
            assert all(elem in [0, 1] for elem in key_bits), "All elements in key_bits must be 0 or 1"
        except AssertionError as error:
            raise ValueError(str(error))

        try:
            assert len(input_bits) == 64, "input_bits must be 64 bits long"
            assert all(elem in [0, 1] for elem in input_bits), "All elements in input_bits must be 0 or 1"
        except AssertionError as error:
            raise ValueError(str(error))

        self.key_schedule = self.key_expansion(key_bits)
        # Initial Permutation of input
        enc_list = self.permutate(input_bits, init_perm_table)

        # Feistel Net ** Repeat 16 times of this round function
        enc_list = self.feistel_net(enc_list, decrypt=False)

        # Final Permutation (Reverse of Initial Permutation)
        enc_list = self.permutate(enc_list, final_perm_table)

        return list_to_binary(enc_list), enc_list

    def decrypt(self, enc_bits, key_bits):
        try:
            assert len(key_bits) == 64, "Key must be 64 bits long"
            assert all(elem in [0, 1] for elem in key_bits), "All elements in key_bits must be 0 or 1"
        except AssertionError as error:
            raise ValueError(str(error))

        try:
            assert len(enc_bits) == 64, "enc_bits must be 64 bits long"
            assert all(elem in [0, 1] for elem in enc_bits), "All elements in enc_bits must be 0 or 1"
        except AssertionError as error:
            raise ValueError(str(error))

        self.key_schedule = self.key_expansion(key_bits)
        # Initial Permutation of input
        dec_list = self.permutate(enc_bits, init_perm_table)

        # Reverse Feistel Net
        dec_list = self.feistel_net(dec_list, decrypt=True)

        # Final Permutation
        dec_list = self.permutate(dec_list, final_perm_table)

        return list_to_binary(dec_list), dec_list
