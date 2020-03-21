# systems-and-network-security
Lectures' implementations.

# How to run ciphers
Inside src/cipher, run `python cipher.py {cipher name} {option} -k {key} {file input} {file output}` 

Options:
- -d : decipher
- -c : cipher

Ciphers:
- cesar

Example to cipher a text using Cesar:

`python cipher.py cesar -c -k 23 clear_text.txt cipher_text.txt`


# How to run crackers
Inside src/cipher, run `python crack.py {cipher method name} {file input} {file output}`

Example to crack a Cesar text:

`python crack.py cesar cipher_text.txt clear_text.txt`
