import sys
from compressor_lzw import compactar_arquivo, descompactar_arquivo

# python compressor_lzw/interface_cli.py compactar arquivos_teste/entrada/teste.txt arquivos_teste/compactados/teste.lzw
# python compressor_lzw/interface_cli.py descompactar arquivos_teste/compactados/teste.lzw arquivos_teste/descompactados/reconstruido.txt

def main():
    if len(sys.argv) != 4:
        print("Uso: python compressor_lzw/interface_cli.py <comando> <entrada> <saida>")
        print("Comandos: compactar | descompactar")
        return

    comando, entrada, saida = sys.argv[1], sys.argv[2], sys.argv[3]

    try:
        if comando == "compactar":
            compactar_arquivo(entrada, saida)
        elif comando == "descompactar":
            descompactar_arquivo(entrada, saida)
        else:
            print("Comando inválido. Use: compactar | descompactar")
    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    main()
