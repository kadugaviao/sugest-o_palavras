class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEndOfWord = False
        self.frequencia = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def inserir_palavra(self, palavra):
        pass

    def remover_palavra(self, palavra):
        pass

    def sugerir_palavra(self, prefixo, max=3):
        pass

    def corretor_inteligente(self, palavra):
        pass