import os

def compactar_arquivo(caminho_entrada: str, caminho_saida: str, tamanho_bloco: int = 4096) -> None:
    dicionario = {bytes([i]): i for i in range(256)}
    proximo_codigo = 256
    sequencia_atual = b""

    with open(caminho_entrada, "rb") as arquivo, open(caminho_saida, "w", encoding="utf-8") as saida:
        while True:
            bloco = arquivo.read(tamanho_bloco)
            if not bloco:
                break

            for byte in bloco:
                nova_sequencia = sequencia_atual + bytes([byte])
                if nova_sequencia in dicionario:
                    sequencia_atual = nova_sequencia
                else:
                    saida.write(str(dicionario[sequencia_atual]) + " ")
                    dicionario[nova_sequencia] = proximo_codigo
                    proximo_codigo += 1
                    sequencia_atual = bytes([byte])

        if sequencia_atual:
            saida.write(str(dicionario[sequencia_atual]) + " ")

    analisar_compressao(caminho_entrada, caminho_saida)

    print(f"Arquivo '{caminho_entrada}' compactado com sucesso para '{caminho_saida}'.")

def descompactar_arquivo(caminho_entrada: str, caminho_saida: str, tamanho_bloco: int = 4096) -> None:
    dicionario = {i: bytes([i]) for i in range(256)}
    proximo_codigo = 256
    sequencia_anterior = None
    buffer = ""

    with open(caminho_entrada, "r", encoding="utf-8") as arquivo, open(caminho_saida, "wb") as saida:
        while True:
            bloco = arquivo.read(tamanho_bloco)
            if not bloco:
                break

            buffer += bloco
            codigos = buffer.split()

            if bloco and not bloco.endswith(" "):
                buffer = codigos.pop()
            else:
                buffer = ""

            for codigo_str in codigos:
                codigo = int(codigo_str)

                if sequencia_anterior is None:
                    entrada = dicionario[codigo]
                elif codigo in dicionario:
                    entrada = dicionario[codigo]
                elif codigo == proximo_codigo:
                    entrada = sequencia_anterior + sequencia_anterior[:1]
                else:
                    raise ValueError("Código inválido encontrado durante a descompressão.")

                saida.write(entrada)

                if sequencia_anterior is not None:
                    dicionario[proximo_codigo] = sequencia_anterior + entrada[:1]
                    proximo_codigo += 1

                sequencia_anterior = entrada

    print(f"Arquivo '{caminho_entrada}' descompactado com sucesso em '{caminho_saida}'.")


def analisar_compressao(arquivo_original: str, arquivo_compactado: str):
    tamanho_original = os.path.getsize(arquivo_original) * 8
    tamanho_compactado = os.path.getsize(arquivo_compactado) * 8
    taxa = 100 - (tamanho_compactado / tamanho_original * 100)
    print(f"- Tamanho original: {tamanho_original} bits")
    print(f"- Tamanho compactado: {tamanho_compactado} bits")
    print(f"- Redução: {taxa:.2f}%\n")
