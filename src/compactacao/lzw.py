import os
import struct

from src.util.arquivos import analisar_compressao
from src.busca.kmp import tabela_prefixos

LIMITE_DICIONARIO = 4096
TAMANHO_BLOCO_ORIGINAL = 1024 * 1024
MAGIC = b"MLZW"
HEADER_FORMAT = ">4sQI"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
INDEX_FORMAT = ">QQI"
INDEX_SIZE = struct.calcsize(INDEX_FORMAT)

def compactar_bloco(dados: bytes) -> bytes:
    dicionario = {bytes([i]): i for i in range(256)}
    proximo_codigo = 256
    sequencia = b""
    saida = bytearray()

    for byte in dados:
        b = bytes([byte])
        nova_seq = sequencia + b
        if nova_seq in dicionario:
            sequencia = nova_seq
        else:
            if sequencia:
                saida.extend(dicionario[sequencia].to_bytes(2, "big"))
            if proximo_codigo < LIMITE_DICIONARIO:
                dicionario[nova_seq] = proximo_codigo
                proximo_codigo += 1
            sequencia = b

    if sequencia:
        saida.extend(dicionario[sequencia].to_bytes(2, "big"))

    return bytes(saida)

def descompactar_bloco(dados: bytes) -> bytes:
    if len(dados) % 2 != 0:
        raise ValueError("Bloco compactado com tamanho inválido.")

    dicionario = {i: bytes([i]) for i in range(256)}
    proximo_codigo = 256
    sequencia_anterior = None
    saida = bytearray()

    i = 0
    while i < len(dados):
        codigo = int.from_bytes(dados[i:i+2], "big")
        i += 2

        if sequencia_anterior is None:
            entrada = dicionario.get(codigo)
            if entrada is None:
                raise ValueError("Código inválido.")
        elif codigo in dicionario:
            entrada = dicionario[codigo]
        elif codigo == proximo_codigo:
            entrada = sequencia_anterior + sequencia_anterior[:1]
        else:
            raise ValueError("Código inválido.")

        saida.extend(entrada)

        if sequencia_anterior is not None and proximo_codigo < LIMITE_DICIONARIO:
            dicionario[proximo_codigo] = sequencia_anterior + entrada[:1]
            proximo_codigo += 1

        sequencia_anterior = entrada

    return bytes(saida)

def ler_header(arquivo):
    dados = arquivo.read(HEADER_SIZE)
    if len(dados) != HEADER_SIZE:
        raise ValueError("Arquivo compactado muito pequeno.")

    magic, tamanho_original, num_blocos = struct.unpack(HEADER_FORMAT, dados)
    if magic != MAGIC:
        raise ValueError("Formato inválido.")

    return tamanho_original, num_blocos


def ler_indice(caminho_arquivo, num_blocos):
    tamanho_arquivo = os.path.getsize(caminho_arquivo)
    index_offset = tamanho_arquivo - num_blocos * INDEX_SIZE
    entradas = []

    with open(caminho_arquivo, "rb") as f:
        f.seek(index_offset)
        for _ in range(num_blocos):
            dados = f.read(INDEX_SIZE)
            if len(dados) != INDEX_SIZE:
                raise ValueError("Índice incompleto.")
            orig_offset, comp_offset, comp_size = struct.unpack(INDEX_FORMAT, dados)
            entradas.append((orig_offset, comp_offset, comp_size))

    entradas.sort(key=lambda e: e[0])
    return entradas

def compactar_arquivo(caminho_entrada, caminho_saida, tamanho_bloco_original=TAMANHO_BLOCO_ORIGINAL):
    indices = []
    tamanho_original = 0
    orig_offset = 0

    with open(caminho_entrada, "rb") as entrada, open(caminho_saida, "wb") as saida:
        saida.write(struct.pack(HEADER_FORMAT, MAGIC, 0, 0))

        while True:
            dados = entrada.read(tamanho_bloco_original)
            if not dados:
                break

            comp_offset = saida.tell()
            dados_comp = compactar_bloco(dados)
            saida.write(dados_comp)
            comp_size = len(dados_comp)

            indices.append((orig_offset, comp_offset, comp_size))
            tamanho_original += len(dados)
            orig_offset += len(dados)

        for orig_offset, comp_offset, comp_size in indices:
            saida.write(struct.pack(INDEX_FORMAT, orig_offset, comp_offset, comp_size))

        saida.seek(0)
        header = struct.pack(HEADER_FORMAT, MAGIC, tamanho_original, len(indices))
        saida.write(header)

    analisar_compressao(caminho_entrada, caminho_saida)

def descompactar_arquivo(caminho_entrada, caminho_saida):
    with open(caminho_entrada, "rb") as arquivo:
        tamanho_original, num_blocos = ler_header(arquivo)

    entradas = ler_indice(caminho_entrada, num_blocos)

    with open(caminho_entrada, "rb") as arquivo, open(caminho_saida, "wb") as saida:
        bytes_escritos = 0

        for orig_offset, comp_offset, comp_size in entradas:
            arquivo.seek(comp_offset)
            dados_comp = arquivo.read(comp_size)
            dados = descompactar_bloco(dados_comp)
            saida.write(dados)
            bytes_escritos += len(dados)

        if bytes_escritos != tamanho_original:
            raise ValueError("Tamanho descompactado inconsistente.")

def buscar_substring_compactado(caminho_arquivo_compactado, substring, encoding="utf-8"):
    padrao = substring.encode(encoding)
    if not padrao:
        raise ValueError("Substring vazia não é permitida.")

    lps = tabela_prefixos(padrao)
    padrao_mv = memoryview(padrao)
    m = len(padrao)

    with open(caminho_arquivo_compactado, "rb") as arquivo:
        tamanho_original, num_blocos = ler_header(arquivo)

    entradas = ler_indice(caminho_arquivo_compactado, num_blocos)
    resultados = []
    j = 0
    pos_global = 0

    with open(caminho_arquivo_compactado, "rb") as arquivo:
        for orig_offset, comp_offset, comp_size in entradas:
            if pos_global != orig_offset:
                pos_global = orig_offset

            arquivo.seek(comp_offset)
            dados_comp = arquivo.read(comp_size)
            dados = descompactar_bloco(dados_comp)
            bloco_mv = memoryview(dados)

            for b in bloco_mv:
                while j > 0 and b != padrao_mv[j]:
                    j = lps[j - 1]
                if b == padrao_mv[j]:
                    j += 1
                    if j == m:
                        resultados.append(pos_global - m + 1)
                        j = lps[m - 1]
                pos_global += 1

    return resultados
