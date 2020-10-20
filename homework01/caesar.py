import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    alphabet="abcdefghijklmnopqrstuvwxyz"
    for i in plaintext:
            if alphabet.find(i.lower())!=-1:
                if i.isupper():
                    ciphertext+=alphabet[(alphabet.find(i.lower())+shift) % len(alphabet)].upper()
                else:
                    ciphertext+=alphabet[(alphabet.find(i)+shift) % len(alphabet)]
            else:
                ciphertext+=i
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    alphabet="abcdefghijklmnopqrstuvwxyz"
    for i in ciphertext:
        if alphabet.find(i.lower())!=-1:
            if i.isupper():
                plaintext+=alphabet[(alphabet.find(i.lower())-shift) % len(alphabet)].upper()
            else:
                plaintext+=alphabet[(alphabet.find(i)-shift) % len(alphabet)]
        else:
            plaintext+=i
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
