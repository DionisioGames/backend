from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def gerar_hash_senha(senha: str):
    return password_hash.hash(senha)


def verificar_senha(senha: str, senha_hash: str):
    return password_hash.verify(senha, senha_hash)