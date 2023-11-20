# DES (Data encryption standard)

This repository is dedicated to the implementation of the Data Encryption Standard (DES). <br>
DES is a symmetric key algorithm used for the encryption of electronic data. <br>
It has historically been widely used in various forms of digital security.
A good reference to understand this algorithm is: <a href="https://csrc.nist.gov/files/pubs/fips/46-3/final/docs/fips46-3.pdf">NIST</a>

## How to Run DES
This module provides a demonstration of the DES algorithm for encryption and decryption of data. <br>

First, clone this repo and move into the Cryptography/des_module directory

```
git clone git@github.com:Snafkin547/Cryptography.git
cd Cryptography/des_module
```

DES in the des.py file is the main body of the algorithm. You may instantiate it and call the '.encrypt' method:

```
DES_inst = DES(key)
enc_val, enc_bits = DES_inst.encrypt(input_bits)
```

DES encryption method needs 'input_bits' as arguments.<br>
The input_bit is required to be 64 bits in a bit-list format like: [0, 1, 0 ... 1]

You may create your own or can use a method in utils.

```
input_bits = generate_bit(64)
```

Putting this all together, you can craft your encryption algorithm like this:
(The last line of assertion proves the symmetric nature of this algorithm)

```
from src import *

key = 8289481480542705629

# Generate 64 bits input
input_val = 3271167758276528483
input_bits = [0, 0, 1, 0, 1, 1, 0, 1, 
          0, 1, 1, 0, 0, 1, 0, 1, 
          1, 0, 0, 0, 0, 1, 0, 1, 
          1, 0, 1, 1, 1, 1, 1, 0, 
          1, 0, 1, 0, 1, 0, 0, 0, 
          1, 1, 0, 0, 1, 0, 0, 0, 
          1, 0, 0, 0, 1, 0, 0, 1, 
          0, 1, 1, 0, 0, 0, 1, 1]

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

```

## Triple-DES

The Data Encryption Standard (DES), a 56-bit encryption algorithm, was broken in record time through a joint effort by the Electronic Frontier Foundation and Distributed.Net.
This significant cryptographic achievement was accomplished in less than 23 hours, specifically in 22 hours and 15 minutes, in January 1999​​​​.  <br>

In response to its vulnerabilities, notably its short key length, an enhanced version called Triple DES (3DES) was introduced, utilizing multiple DES keys in sequence to significantly bolster security. 
This advanced version has gained approval from the National Institute of Standards and Technology (NIST) and is incorporated in numerous cryptographic standards, maintaining its relevance as a secure option for protecting sensitive data, particularly in legacy systems.

The following is the example code to demonstrate triple-DES algorithm:

```
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
```

## Code Formatting Standards
My project uses Black, a Python code formatter, to ensure uniform formatting across our codebase. 
Contributors are required to format their code using black . in the root directory before pushing to the repository. 

Additionally, we employ a GitHub Action that automatically checks for compliance with Black's formatting standards on each pull request. 
This check can prevent merging if the code does not meet the required standards. 
It's crucial to remember to run Black before pushing changes, as this not only keeps the code clean and readable but also facilitates the review and merging process by adhering to our automated checks.
