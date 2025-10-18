import sys
from compressor_lzw import compactar_arquivo_em_blocos, descompactar_arquivo_em_blocos

# python compressor_lzw/interface_cli.py compactar seu_arquivo.txt seu_arquivo.lzw
# python compressor_lzw/interface_cli.py descompactar seu_arquivo.lzw arquivo_reconstruido.txt

def main():
    if len(sys.argv) != 4:
        print("Uso: python compressor_lzw/interface_cli.py <comando> <entrada> <saida>")
        print("Comandos: compactar | descompactar")
        return

    comando, entrada, saida = sys.argv[1], sys.argv[2], sys.argv[3]

    try:
        if comando == "compactar":
            compactar_arquivo_em_blocos(entrada, saida)
        elif comando == "descompactar":
            descompactar_arquivo_em_blocos(entrada, saida)
        else:
            print("Comando inválido. Use: compactar | descompactar")
    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    main()
