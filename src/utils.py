"""
utils.py
--------
Funções de apoio (puras, sem depender da TRIE) usadas pela árvore.

- normalizar_texto(texto): padroniza o texto para a árvore -> passa para
  minúsculas, remove espaços das pontas e remove acentuação e o "ç"
  (usando decomposição Unicode NFKD e descartando os sinais combinantes).
  Ex.: "Coração" -> "coracao".

- distancia_levenshtein(palavra_a, palavra_b): retorna o número mínimo de
  edições (inserir, remover ou substituir 1 caractere) para transformar uma
  palavra na outra, via programação dinâmica (matriz (m+1)x(n+1)). Quanto
  menor o valor, mais parecidas as palavras. É a base do corretor ortográfico.
"""

from __future__ import annotations

import unicodedata


def normalizar_texto(texto: str) -> str:
    texto = texto.lower().strip()
    decomposto = unicodedata.normalize("NFKD", texto)
    sem_acentos = "".join(
        caractere
        for caractere in decomposto
        if not unicodedata.combining(caractere)
    )
    return sem_acentos


def distancia_levenshtein(palavra_a: str, palavra_b: str) -> int:
    m, n = len(palavra_a), len(palavra_b)
    dp: list[list[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            custo = 0 if palavra_a[i - 1] == palavra_b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + custo,
            )

    return dp[m][n]