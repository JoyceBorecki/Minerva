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

### Interação 3

- **Data:** 19/10/2025  
- **Etapa do Projeto:** 1 - Compressão de Arquivos  
- **Ferramenta de IA Utilizada:** ChatGPT  
- **Objetivo da Consulta:** Verificar o comportamento real da compressão em um arquivo grande e identificar problemas no código original.

- **Contexto:**
Para testar o algoritmo em um cenário mais realista, decidi usar um arquivo de texto extenso: o livro **"Quincas Borba"** de Machado de Assis, disponível em domínio público.  
Baixei o texto em formato **Plain Text UTF-8 (~481 KB)** e salvei como `livro.txt` dentro da pasta `arquivos_teste/entrada`.
Depois disso, rodei o programa duas vezes: primeiro com a **versão original do código**, e depois com a **versão corrigida sugerida pela IA**, para comparar os resultados e entender o que estava acontecendo.

- **Prompt(s) Utilizado:**
1. "O código parece estar funcionando, mas a taxa de compressão está negativa mesmo em arquivos grandes. Pode estar errado?"  
2. "Como posso melhorar a forma como os códigos são salvos para reduzir o tamanho do arquivo compactado?"  
3. "Pode revisar a lógica e explicar por que a memória não muda?"

- **Resumo da Resposta da IA:**
A IA apontou que a versão original do código tinha dois problemas:

- Os códigos estavam sendo gravados como **texto decimal separado por espaços**, o que aumentava muito o tamanho final do arquivo e impedia que a compressão funcionasse de verdade.  
- O dicionário crescia indefinidamente, sem um limite, o que podia aumentar o consumo de memória e gerar códigos cada vez maiores.

Para resolver, foram sugeridas três mudanças importantes:

1. Gravar os códigos em **formato binário com tamanho fixo de 2 bytes**, reduzindo drasticamente o tamanho do arquivo compactado.  
2. **Limitar o dicionário a 4096 entradas**, garantindo que o uso de memória fique constante.  
3. Continuar a leitura em **blocos de 4 KB**, o que mantém o desempenho mesmo em arquivos grandes.

- **Resultado do teste com `livro.txt`:**
O print mostra os resultados ao executar os dois códigos com o mesmo arquivo:

![Resultados](data/exemplos/img_ref.PNG)

O primeiro resultado (acima) é da versão **original**, que teve taxa de compressão **-15,61%**, ou seja, o arquivo compactado ficou ainda maior que o original.  
O segundo resultado (abaixo) é da versão **corrigida sugerida pela IA**, que reduziu o tamanho em cerca de **33,56%**, gerando um arquivo final com **327.456 bytes**, provando que a compressão passou a funcionar corretamente.

- **Análise e Aplicação:**
Esse teste foi importante para perceber que o problema não estava no algoritmo LZW em si, mas **na forma como ele estava sendo implementado**.  
Mesmo com um arquivo grande e repetitivo, a compressão ficava negativa porque os códigos eram gravados como texto e o dicionário não tinha limite.
Com as correções aplicadas, a compressão passou a gerar ganho real, e o uso de memória se manteve constante.  
Esse experimento também confirmou, na prática, o que já havia sido discutido na **Interação 1**: ler o arquivo em blocos de 4 KB permite processar arquivos grandes sem sobrecarregar a memória.

- **Referência no Código:**
As melhorias foram implementadas nas funções `compactar_arquivo()` e `descompactar_arquivo()` do arquivo `compressor_lzw.py`.  
A função `analisar_compressao()` continua responsável por calcular a taxa de compressão e comparar os tamanhos original e compactado.

---