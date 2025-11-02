# Changelog — Minerva

Todas as alterações notáveis deste projeto serão documentadas neste arquivo.  
O formato segue as boas práticas do [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),  
e este projeto adota o [versionamento semântico](https://semver.org/lang/pt-BR/).

---

## [v1.0.0-beta] — 2025-11-01
### Adicionado
- Implementação completa da **Etapa 1 e Etapa 2** do projeto.
- Criação da **CLI (`run.py`)** com suporte aos comandos principais:
  - `compactar <arquivo.txt>` — compactação via **LZW**.
  - `descompactar <arquivo.lzw>` — descompactação reversa.
  - `buscar_simples <arquivo.txt> "<substring>"` — busca com **Knuth-Morris-Pratt (KMP)**.
- Estrutura modular em `src/`:
  - `compactacao/lzw.py` — algoritmos de compressão e descompressão.
  - `busca/kmp.py` — algoritmo de busca eficiente.
  - `util/arquivos.py` e `util/memoria.py` — análise de desempenho, hash e uso de memória.
- Empacotamento do executável único **`minerva.exe`** com **PyInstaller**.
- Verificação de integridade dos arquivos via hash SHA-256.
- Cálculo automático da taxa de compressão.
- Log de uso de IA (`AI_USAGE_LOG.md`) documentando interações com assistentes generativos.

### Alterado
- Refatoração da CLI (`cli.py`) para melhor tratamento de erros e mensagens de status.
- Organização dos diretórios em `src/` e `data/` (entrada, compactados e descompactados).

### Conhecido / Próximos passos
- Início do planejamento da **Etapa 3** — implementação de busca binária otimizada e indexação.
- Portabilidade testada no **Windows**; compatibilidade com **Linux/macOS** será adicionada na próxima versão.

---

## Histórico
- **2025-11-01** — Publicação da primeira release (`v1.0.0`).

---

> *Minerva é uma ferramenta CLI para compressão e busca de substrings em arquivos de texto grandes.*
