import os
import hashlib

def calcular_hash(caminho_arquivo):
    sha256 = hashlib.sha256()
    with open(caminho_arquivo, "rb") as f:
        for bloco in iter(lambda: f.read(4096), b""):
            sha256.update(bloco)
    return sha256.hexdigest()

def analisar_compressao(arquivo_original: str, arquivo_compactado: str):
    tamanho_original = os.path.getsize(arquivo_original)
    tamanho_compactado = os.path.getsize(arquivo_compactado)
    if tamanho_original == 0:
        print("- Arquivo vazio (0 bytes)")
        return
    taxa = 100 - (tamanho_compactado / tamanho_original * 100)
    print(f"- Tamanho original: {tamanho_original} bytes")
    print(f"- Tamanho compactado: {tamanho_compactado} bytes")
    print(f"- Redução: {taxa:.2f}%\n")
