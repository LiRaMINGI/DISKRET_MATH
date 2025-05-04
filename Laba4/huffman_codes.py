from __future__ import annotations

import heapq


class Node:
    def __init__(
        self,
        char: str | None = None, #Символ
        freq: float = 0,  #Частота
        left: Node | None = None, #левый и правый дочерние узлы
        right: Node | None = None,
    ):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other): #функция сравнения частот
        return self.freq < other.freq


def huffman_encode(text: str, freq_dict: dict[str, int]) -> str: #Принимает текст и словарь частот символов
    """Кодируем строку по алгоритму Хаффмана."""
    codes = _compress_by_huffman_codes(freq_dict)

    return "".join(codes[ch] for ch in text if ch in codes) #Возвращает строку из битов (0 и 1)


def _compress_by_huffman_codes(freq_dict: dict[str, int]) -> dict[str, str]:
    """
    Формируем коды Хаффмана.

    Возвращает словарь {символ: код Хаффмана}.
    """
    # Строим дерево Хаффмана
    root = _build_huffman_tree(freq_dict)
    # Присваиваем коды
    codes = _assign_codes(root)
    return codes


def _build_huffman_tree(freq_dict: dict[str, int]) -> Node:
    """Строим дерево Хаффмана по словарю частот."""

    heap = []
    # Создаём узлы для каждого символа и добавляем их в кучу
    for char, freq in freq_dict.items():   #Создаем начальные узлы и помещаем их в кучу
        heapq.heappush(heap, Node(char, freq))

    # Объединяем два узла с наименьшей частотой до получения одного корня
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = Node(None, node1.freq + node2.freq, node1, node2)
        heapq.heappush(heap, merged)

    return heap[0]


def _assign_codes(node: Node, code: str = "", code_dict: dict | None = None) -> dict[str, str]:
    if code_dict is None: #Если code_dict не передан (первый вызов функции),
        code_dict = {}  # создаётся пустой словарь.

    if node is None: #тупиковый случай
        return code_dict

    if node.char is not None: # Проверяет, содержит ли узел символ (листовой узел)
        code_dict[node.char] = code or "0"
    else:
        _assign_codes(node.left, code + "0", code_dict)
        _assign_codes(node.right, code + "1", code_dict)

    return code_dict
