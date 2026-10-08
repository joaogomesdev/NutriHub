from pwdlib import PasswordHash

 # Proteção de senha com o Hash

passaword_hash = PasswordHash.recommended() # Objeto responsável pelo nosso sistema de hash

def criar_hash(senha: str):
    return passaword_hash.hash(senha)

def verificar_senha(senha, hash):
    return passaword_hash.verify(senha, hash)