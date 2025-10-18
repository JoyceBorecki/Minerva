# Compacta um arquivo de texto usando o algoritmo lzw
def compactar_arquivo(caminho_entrada: str, caminho_saida: str) -> None:
    dicionario = {chr(i): i for i in range(256)}
    proximo_codigo = 256

    sequencia_atual = ""
    codigos_saida = []

    with open(caminho_entrada, "r", encoding="utf-8") as arquivo:
        texto = arquivo.read()

    for caractere in texto:
        nova_sequencia = sequencia_atual + caractere

        if nova_sequencia in dicionario:
            sequencia_atual = nova_sequencia
        else:
            codigos_saida.append(dicionario[sequencia_atual])
            dicionario[nova_sequencia] = proximo_codigo
            proximo_codigo += 1
            sequencia_atual = caractere

    if sequencia_atual:
        codigos_saida.append(dicionario[sequencia_atual])

    with open(caminho_saida, "w", encoding="utf-8") as saida:
        saida.write(" ".join(map(str, codigos_saida)))

    print(f"Arquivo '{caminho_entrada}' compactado com sucesso para '{caminho_saida}'.")

# Descompacta um arquivo gerado pelo lzw e reconstrói o texto
def descompactar_arquivo(caminho_entrada: str, caminho_saida: str) -> None:
    with open(caminho_entrada, "r", encoding="utf-8") as arquivo:
        codigos = list(map(int, arquivo.read().split()))

    dicionario = {i: chr(i) for i in range(256)}
    proximo_codigo = 256

    sequencia_anterior = dicionario[codigos[0]]
    texto_saida = [sequencia_anterior]

    for codigo in codigos[1:]:
        if codigo in dicionario:
            entrada = dicionario[codigo]
        elif codigo == proximo_codigo:
            entrada = sequencia_anterior + sequencia_anterior[0]
        else:
            raise ValueError("Código inválido encontrado durante a descompressão.")

        texto_saida.append(entrada)
        dicionario[proximo_codigo] = sequencia_anterior + entrada[0]
        proximo_codigo += 1
        sequencia_anterior = entrada

    with open(caminho_saida, "w", encoding="utf-8") as saida:
        saida.write("".join(texto_saida))

    print(f"Arquivo '{caminho_entrada}' descompactado com sucesso em '{caminho_saida}'.")
