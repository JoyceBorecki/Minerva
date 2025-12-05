# Minerva

Minerva é uma ferramenta de linha de comando (CLI) desenvolvida para compressão e busca de substrings em arquivos de texto grandes, mesmo quando o tamanho do arquivo ultrapassa a memória RAM disponível.

## Compressão de Arquivos Grandes (LZW)

A compressão utiliza o algoritmo **Lempel-Ziv-Welch (LZW)** para reduzir o tamanho de arquivos de texto de forma sequencial e sem perdas.
Durante o processo, o arquivo é lido em blocos de bytes, e um dicionário é construído dinamicamente para codificar padrões recorrentes.
A descompressão reconstrói o arquivo original com base na mesma estrutura e limites de dicionário.

**Comandos:**
```bash
python run.py compactar <arquivo.txt>
python run.py descompactar <arquivo.lzw>
```

**Características:**
- Processamento por blocos, sem carregar o arquivo inteiro na memória.
- Dicionário limitado a 4096 entradas.
- Verificação de integridade via hash SHA-256 após a descompressão.
- Exibição da taxa de compressão e uso de memória.

## Busca de Substring em Arquivo Grande (KMP)

A busca de substrings é implementada com o algoritmo **Knuth-Morris-Pratt (KMP)**, que oferece desempenho linear e baixo consumo de memória.
O método identifica padrões mesmo quando cruzam fronteiras de blocos, preservando as posições exatas (offsets) em bytes dentro do arquivo original.

**Comando:**
```bash
python run.py buscar_simples <arquivo.txt> "<substring>"
```

**Características:**
- Busca sem carregar o arquivo completo na memória.
- Detecta ocorrências que cruzam limites de blocos.
- Exibe os offsets em bytes das ocorrências encontradas.
- Mantém uso de memória constante, independentemente do tamanho do arquivo.

## Busca no Arquivo Compactado (KMP + LZW por blocos)

A etapa 3 integra as anteriores, permitindo buscar substrings **diretamente** no arquivo compactado. O arquivo passa a ser organizado em blocos e acompanhado de um índice, o que permite acessar apenas as partes necessárias.
Durante a busca, o programa lê apenas o índice e descompacta cada bloco individualmente, aplicando o algoritmo KMP de forma contínua. Assim, a busca permanece eficiente e encontra ocorrências mesmo quando a substring atravessa dois blocos diferentes.

**Comando:**
```bash
python run.py buscar_compactado <arquivo.lzw> "<substring>"
```

**Características:**
- Permite busca diretamente no arquivo compactado, sem descompactação total.
- Carrega apenas o índice e um bloco por vez na memória.
- Mantém uso de memória baixo e constante, independentemente do tamanho do arquivo.

## Uso de Inteligência Artificial

Ferramentas de IA generativa foram utilizadas apenas como apoio na estruturação de código, revisão de lógica e formatação do relatório. Todas as interações foram registradas no arquivo `AI_USAGE_LOG.md`.