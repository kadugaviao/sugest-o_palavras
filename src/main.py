"""
main.py
-------
Interface interativa do sistema de autocompletar com TRIE.
O usuário DIGITA um prefixo e recebe as sugestões na hora (como em um
buscador ou teclado de celular). Quando o prefixo não casa com nada,
o sistema usa o corretor ortográfico para sugerir a palavra mais
próxima ("você quis dizer..."). Também permite inserir e remover palavras.

- mostrar_menu(): imprime as opções disponíveis.
- main(): cria a Trie e roda o laço principal, chamando inserir_palavra,
  remover_palavra, sugerir_palavra e, como fallback, sugerir_correcao.
"""

from __future__ import annotations

from trie import Trie


def mostrar_menu() -> None:
    print("\n--- AUTOCOMPLETAR (TRIE) ---")
    print("1 - Digitar prefixo e ver sugestões")
    print("2 - Inserir palavra(s)")
    print("3 - Remover palavra(s)")
    print("4 - Sair")


def main() -> None:
    trie = Trie()
    print("Sistema iniciado com uma lista de palavras de teste.")

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            prefixo = input("Digite o prefixo: ").strip()
            sugestoes = trie.sugerir_palavra(prefixo, max=5)

            if sugestoes:
                print("Sugestões:")
                for i, palavra in enumerate(sugestoes, start=1):
                    print(f"  {i}. {palavra}")
            else:
                # Nenhuma palavra começa com esse prefixo:
                # cai no corretor e mostra só a correção mais provável.
                correcoes = trie.sugerir_correcao(prefixo, max=1)
                if correcoes:
                    print(f"'{prefixo}' não encontrada. Você quis dizer: {correcoes[0]}?")
                else:
                    print(f"Nenhuma palavra encontrada para '{prefixo}'.")

        elif opcao == "2":
            entrada = input("Palavra(s) a inserir (separe por vírgula): ")
            palavras = [p.strip() for p in entrada.split(",") if p.strip()]
            trie.inserir_palavra(palavras)
            print(f"Inserido: {palavras}")

        elif opcao == "3":
            entrada = input("Palavra(s) a remover (separe por vírgula): ")
            palavras = [p.strip() for p in entrada.split(",") if p.strip()]
            trie.remover_palavra(palavras)
            print(f"Removido (se existia): {palavras}")

        elif opcao == "4":
            print("Encerrando. Até mais!")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()