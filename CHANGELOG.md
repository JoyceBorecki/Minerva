# Changelog — Minerva

Todas as alterações notáveis deste projeto serão documentadas neste arquivo.  
O formato segue as boas práticas do [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),  
e este projeto adota o [versionamento semântico](https://semver.org/lang/pt-BR/).

---

## [v2.0.0] — 2025-12-05
### Adicionado
- Implementação completa da **Etapa 3**: busca de substring diretamente no arquivo compactado.
- Novo formato de arquivo `.lzw` com:
  - compressão por blocos;
  - índice contendo offsets originais e compactados;
  - suporte à leitura seletiva dos blocos.
- Algoritmo de busca adaptado para operar em dados descompactados por streaming, preservando offsets corretos.
- Ajustes na CLI para suportar:
  - `buscar_compactado <arquivo.lzw> "<substring>"`.
- Atualização do executável `run.exe` com todos os recursos das três etapas.

### Alterado
- Refatoração do módulo `compactacao/lzw.py` para suportar compressão e descompressão em blocos indexados.
- Atualização do README e demais documentações para incluir a Etapa 3.

---

## [v1.0.0] — 2025-11-01
### Adicionado
- Implementação da **Etapa 1 (LZW)** e **Etapa 2 (busca simples com KMP)**.
- Criação da CLI com suporte aos comandos:
  - `compactar <arquivo.txt>`
  - `descompactar <arquivo.lzw>`
  - `buscar_simples <arquivo.txt> "<substring>"`
- Estrutura modular do projeto (`src/compactacao`, `src/busca`, `src/util`).
- Empacotamento inicial como executável Windows via PyInstaller.
- Verificação de integridade por hash SHA-256 e relatório de taxa de compressão.

---

## Histórico
- **2025-11-01** — Publicação da primeira release (`v1.0.0`).
- **2025-12-05** — Release da versão completa com suporte às 3 etapas (`v2.0.0`).

---

> *Minerva é uma ferramenta CLI para compressão e busca de substrings em arquivos de texto grandes.*
