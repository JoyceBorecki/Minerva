from src.util.arquivos import analisar_compressao
import os

LIMITE_DICIONARIO = 4096

def compactar_arquivo(caminho_entrada: str, caminho_saida: str, tamanho_bloco: int = 4096) -> None:
    dicionario = {bytes([i]): i for i in range(256)}
    proximo_codigo = 256
    sequencia_atual = b""

    with open(caminho_entrada, "rb") as arquivo, open(caminho_saida, "wb") as saida:
        while True:
            bloco = arquivo.read(tamanho_bloco)
            if not bloco:
                break

            for byte in bloco:
                nova_sequencia = sequencia_atual + bytes([byte])
                if nova_sequencia in dicionario:
                    sequencia_atual = nova_sequencia
                else:
                    if sequencia_atual:
                        saida.write(dicionario[sequencia_atual].to_bytes(2, byteorder="big"))
                    if proximo_codigo < LIMITE_DICIONARIO:
                        dicionario[nova_sequencia] = proximo_codigo
                        proximo_codigo += 1
                    sequencia_atual = bytes([byte])

        if sequencia_atual:
            saida.write(dicionario[sequencia_atual].to_bytes(2, byteorder="big"))

    analisar_compressao(caminho_entrada, caminho_saida)
    print(f"Arquivo '{caminho_entrada}' compactado com sucesso para '{caminho_saida}'.")


def descompactar_arquivo(caminho_entrada: str, caminho_saida: str, tamanho_bloco: int = 4096) -> None:
    dicionario = {i: bytes([i]) for i in range(256)}
    proximo_codigo = 256
    sequencia_anterior = None
    buffer = b""

    with open(caminho_entrada, "rb") as arquivo, open(caminho_saida, "wb") as saida:
        while True:
            bloco = arquivo.read(tamanho_bloco)
            if not bloco and len(buffer) < 2:
                break

            buffer += bloco
            limite_leitura = len(buffer) - (len(buffer) % 2)
            i = 0
            while i < limite_leitura:
                codigo = int.from_bytes(buffer[i:i+2], byteorder="big")
                i += 2

                if sequencia_anterior is None:
                    entrada = dicionario[codigo]
                elif codigo in dicionario:
                    entrada = dicionario[codigo]
                elif codigo == proximo_codigo:
                    entrada = sequencia_anterior + sequencia_anterior[:1]
                else:
                    raise ValueError("Código inválido encontrado durante a descompressão.")

                saida.write(entrada)

                if sequencia_anterior is not None and proximo_codigo < LIMITE_DICIONARIO:
                    dicionario[proximo_codigo] = sequencia_anterior + entrada[:1]
                    proximo_codigo += 1

                sequencia_anterior = entrada

            buffer = buffer[limite_leitura:]

    print(f"Arquivo '{caminho_entrada}' descompactado com sucesso em '{caminho_saida}'.")
