"""
trie.py
-------
Árvore TRIE para autocompletar palavras. Importa normalizar_texto e
distancia_levenshtein do utils.py.

Classes:
- TrieNode: um nó da árvore. Guarda 'filhos' ({letra: TrieNode}),
  'fim_de_palavra' (se um caminho termina ali formando palavra válida) e
  'frequencia' (quantas vezes a palavra foi inserida).

- Trie: a árvore em si. Nasce com uma lista básica de palavras de teste.
  Métodos:
    * inserir_palavra(palavra): aceita string OU lista. Desce/cria os nós e,
      no fim, marca a palavra e incrementa a frequência (+1 se já existir).
    * remover_palavra(palavra): aceita string OU lista. Fail-safe: se a
      palavra não existe, não gera erro. Desmarca o fim e apaga os nós que
      ficaram inúteis (via _remover_recursivo).
    * sugerir_palavra(prefixo, max=3): vai até o nó do prefixo, coleta as
      palavras a partir dali e retorna até 'max' ordenadas por frequência
      (maior->menor) e, no empate, por ordem alfabética.
    * sugerir_correcao(palavra, max=3, distancia_maxima=3): corretor
      ortográfico (extra). Usa a distância de Levenshtein para achar as
      palavras mais próximas da digitada, ignorando as que estão mais
      distantes que 'distancia_maxima'. Ordena por 3 critérios: distância,
      frequência e alfabético.
    * auxiliares internos: _remover_recursivo, _buscar_no, _coletar_palavras
      (DFS que junta (palavra, frequencia)) e _listar_todas.
"""

from __future__ import annotations

from utils import normalizar_texto, distancia_levenshtein


class TrieNode:
    def __init__(self) -> None:
        self.filhos: dict[str, TrieNode] = {}
        self.fim_de_palavra: bool = False
        self.frequencia: int = 0


class Trie:
    def __init__(self, palavras_iniciais: list[str] | None = None) -> None:
        self.raiz: TrieNode = TrieNode()

        if palavras_iniciais is None:
            palavras_iniciais = [
                "casa", "casaco", "carro",
                "cachorro", "casal", "cartografia",
                "caminho", "camisa", "cafe", "caderno",
            ]
        self.inserir_palavra(palavras_iniciais)

    def inserir_palavra(self, palavra: str | list[str]) -> None:
        if isinstance(palavra, list):
            for item in palavra:
                self.inserir_palavra(item)
            return

        palavra = normalizar_texto(palavra)
        if not palavra:
            return

        no = self.raiz
        for letra in palavra:
            if letra not in no.filhos:
                no.filhos[letra] = TrieNode()
            no = no.filhos[letra]

        no.fim_de_palavra = True
        no.frequencia += 1

    def remover_palavra(self, palavra: str | list[str]) -> None:
        if isinstance(palavra, list):
            for item in palavra:
                self.remover_palavra(item)
            return

        palavra = normalizar_texto(palavra)
        if not palavra:
            return

        self._remover_recursivo(self.raiz, palavra, profundidade=0)

    def _remover_recursivo(
        self, no: TrieNode, palavra: str, profundidade: int
    ) -> bool:
        if profundidade == len(palavra):
            if no.fim_de_palavra:
                no.fim_de_palavra = False
                no.frequencia = 0
            return len(no.filhos) == 0

        letra = palavra[profundidade]
        filho = no.filhos.get(letra)

        if filho is None:
            return False

        pode_apagar_filho = self._remover_recursivo(
            filho, palavra, profundidade + 1
        )

        if pode_apagar_filho:
            del no.filhos[letra]

        return len(no.filhos) == 0 and not no.fim_de_palavra

    def sugerir_palavra(self, prefixo: str, max: int = 3) -> list[str]:
        prefixo = normalizar_texto(prefixo)

        no = self._buscar_no(prefixo)
        if no is None:
            return []

        encontradas: list[tuple[str, int]] = []
        self._coletar_palavras(no, prefixo, encontradas)

        encontradas.sort(key=lambda item: (-item[1], item[0]))

        return [palavra for palavra, _ in encontradas[:max]]

    def sugerir_correcao(
        self, palavra: str, max: int = 3, distancia_maxima: int = 3
    ) -> list[str]:
        palavra = normalizar_texto(palavra)

        todas = self._listar_todas(self.raiz, "")

        ranking = [
            (p, distancia_levenshtein(palavra, p), freq)
            for p, freq in todas
        ]

        ranking = [item for item in ranking if item[1] <= distancia_maxima]

        ranking.sort(key=lambda item: (item[1], -item[2], item[0]))

        return [p for p, _, _ in ranking[:max]]

    def _buscar_no(self, prefixo: str) -> TrieNode | None:
        no = self.raiz
        for letra in prefixo:
            if letra not in no.filhos:
                return None
            no = no.filhos[letra]
        return no

    def _coletar_palavras(
        self,
        no: TrieNode,
        prefixo: str,
        acumulador: list[tuple[str, int]],
    ) -> None:
        if no.fim_de_palavra:
            acumulador.append((prefixo, no.frequencia))

        for letra, filho in no.filhos.items():
            self._coletar_palavras(filho, prefixo + letra, acumulador)

    def _listar_todas(
        self, no: TrieNode, prefixo: str
    ) -> list[tuple[str, int]]:
        resultado: list[tuple[str, int]] = []
        self._coletar_palavras(no, prefixo, resultado)
        return resultado