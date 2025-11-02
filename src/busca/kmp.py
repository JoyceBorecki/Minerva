from typing import Iterator, List

def tabela_prefixos(padrao: bytes) -> List[int]:
    lps = [0] * len(padrao)
    j = 0

    for i in range(1, len(padrao)):
        while j > 0 and padrao[i] != padrao[j]:
            j = lps[j - 1]
        if padrao[i] == padrao[j]:
            j += 1
            lps[i] = j
    return lps


def iter_busca_kmp(
    caminho_arquivo: str,
    padrao_bytes: bytes,
    tamanho_bloco: int = 8 << 20,
) -> Iterator[int]:

    if not padrao_bytes:
        raise ValueError("Substring vazia não é permitida.")

    m = len(padrao_bytes)
    lps = tabela_prefixos(padrao_bytes)

    padrao_mv = memoryview(padrao_bytes)
    j = 0
    pos_global = 0

    with open(caminho_arquivo, "rb") as f:
        while True:
            bloco = f.read(tamanho_bloco)
            if not bloco:
                break

            bloco_mv = memoryview(bloco)
            for b in bloco_mv:
                while j > 0 and b != padrao_mv[j]:
                    j = lps[j - 1]
                if b == padrao_mv[j]:
                    j += 1
                    if j == m:
                        yield pos_global - m + 1
                        j = lps[m - 1]
                pos_global += 1


def buscar_substring(
    caminho_arquivo: str,
    substring: str,
    tamanho_bloco: int = 8 << 20,
    encoding: str = "utf-8",
) -> List[int]:
    padrao_bytes = substring.encode(encoding)
    return list(iter_busca_kmp(caminho_arquivo, padrao_bytes, tamanho_bloco))
