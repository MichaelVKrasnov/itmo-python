def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key = keyword.lower()
    alphabet="abcdefghijklmnopqrstuvwxyz"
    i1=0
    for i in plaintext:
            if alphabet.find(i.lower())!=-1:
                if i.isupper():
                    ciphertext+=alphabet[(alphabet.find(i.lower())+alphabet.find(key[i1 % len(key)])) % 26].upper()
                else:
                    ciphertext+=alphabet[(alphabet.find(i)+alphabet.find(key[i1 % len(key)])) % 26]
            else:
                ciphertext+=i
            i1+=1
    return ciphertext
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key = keyword.lower()
    i1=0
    alphabet="abcdefghijklmnopqrstuvwxyz"
    for i in ciphertext:
        if alphabet.find(i.lower())!=-1:
            if i.isupper():
                plaintext+=alphabet[(alphabet.find(i.lower())-alphabet.find(key[i1 % len(key)])) % 26].upper()
            else:
                plaintext+=alphabet[(alphabet.find(i)-alphabet.find(key[i1 % len(key)])) % 26]
        else:
            plaintext+=i
        i1+=1
    return plaintext
