### Interação 1

- **Data:** 18/10/2025
- **Etapa do Projeto:** 1 - Compressão de Arquivos
- **Ferramenta de IA Utilizada:** ChatGPT
- **Objetivo da Consulta:** Eu queria entender por que usamos 4096 bytes (4 KB) como tamanho de bloco ao ler arquivos grandes e o que muda se eu aumentar ou diminuir esse valor.

- **Prompt(s) Utilizado(s):**
  1. "Por que ler 4 KB e não mais e não menos?"
  2. "Cada bloco deve ser dividido em 4 KB mesmo que o arquivo tenha 1 GB?"
  3. "O que aconteceria se eu aumentasse ou diminuísse o tamanho do bloco?"

- **Resumo da Resposta da IA:**
  A IA explicou que 4 KB é o tamanho de página padrão da memória RAM na maioria dos sistemas operacionais, por isso essa escolha costuma ser mais eficiente. Em vez de carregar o arquivo inteiro na memória, o programa lê e processa o conteúdo em blocos de 4 KB, mantendo o uso de memória constante mesmo em arquivos muito grandes. Por exemplo, um arquivo de 1 GB será dividido automaticamente em cerca de 250 mil blocos de 4 KB, processados um de cada vez.
  Se eu aumentar o tamanho do bloco (por exemplo, para 8 KB ou 16 KB), o programa fará menos leituras e pode ficar um pouco mais rápido, mas vai usar mais memória temporária.
  Se eu diminuir (por exemplo, para 1 KB), o consumo de memória será ainda menor, mas o número de leituras aumenta e a compressão pode ficar mais lenta.
  Por isso, 4 KB costuma ser um bom equilíbrio entre desempenho e uso de memória.

- **Análise e Aplicação:**
  Essa explicação me ajudou a entender a relação entre tamanho do bloco, velocidade e consumo de memória. Mantive 4 KB como valor padrão (tamanho_bloco=4096) no código, pois é a opção mais equilibrada para a maioria dos casos. Agora também sei que posso mudar esse valor: usar blocos maiores em máquinas com bastante memória ou blocos menores em máquinas com pouca RAM.

- **Referência no Código:**
  A leitura em blocos está implementada nas funções compactar_arquivo_em_blocos() e descompactar_arquivo_em_blocos() no arquivo compressor_lzw.py.
  
---

### Interação 2

- **Data:** 18/10/2025
- **Etapa do Projeto:** 1 - Compressão de Arquivos
- **Ferramenta de IA Utilizada:** ChatGPT
- **Objetivo da Consulta:** Entender por que arquivos muito pequenos podem ficar maiores após a compressão com LZW.

- **Prompt(s) Utilizado(s):**
  1. "Por que o arquivo ABRACADABRA! ficou maior depois de compactar?"
  2. "É normal a taxa de compressão ser negativa em arquivos pequenos?"

- **Resumo da Resposta da IA:**
  A IA explicou que isso é normal em algoritmos como LZW e Huffman quando o arquivo é muito pequeno. No caso do arquivo teste2.txt, ABRACADABRA! (12 caracteres, 96 bits), a versão compactada acabou com 256 bits. Acontece porque o algoritmo precisa criar um dicionário e representar as sequências com códigos numéricos, e essa estrutura tem um custo extra que só compensa quando o arquivo é maior.
  Arquivos pequenos: têm pouca repetição e não trazem vantagem para a compressão, às vezes ficando até maiores.
  Arquivos grandes e repetitivos: a compressão funciona melhor, pois o dicionário aproveita os padrões e o tamanho total diminui.

- **Análise e Aplicação:**
  Esse teste com ABRACADABRA! ajudou a entender que o LZW não é vantajoso para arquivos muito pequenos. Eles podem até aumentar de tamanho, e isso é esperado. Já em arquivos maiores e com padrões repetidos (teste.txt (~80 KB)) a compressão reduziu o tamanho em cerca de 25%.

- **Referência no Código:**
  A comparação entre tamanho original e compactado é feita pela função analisar_compressao() no arquivo compressor_lzw.py.

---