from __future__ import annotations
import heapq
from collections import Counter
from typing import Dict, Tuple


class Node:
    def __init__(
            self,
            pair: Tuple[str, str] | None = None,
            freq: int = 0,
            left: Node | None = None,
            right: Node | None = None,
    ):
        self.pair = pair  # Пара символов (например, ('a', 'b'))
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: Node) -> bool:
        return self.freq < other.freq


def build_pair_frequencies(text: str) -> Dict[Tuple[str, str], int]:
    """Считает частоты пар символов с перекрытием (биграмм)."""
    pairs = [
        (text[i], text[i + 1])
        for i in range(len(text) - 1)
    ]
    return Counter(pairs)


def build_huffman_tree(freq_dict: Dict[Tuple[str, str], int]) -> Node:
    """Строит дерево Хаффмана для пар символов."""
    heap = []
    for pair, freq in freq_dict.items():
        heapq.heappush(heap, Node(pair, freq))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)

    return heap[0]


def assign_codes(node: Node, prefix: str = "", codes: Dict[Tuple[str, str], str] | None = None) -> Dict[
    Tuple[str, str], str]:
    """Генерирует коды Хаффмана для пар символов."""
    if codes is None:
        codes = {}

    if node.pair is not None:
        codes[node.pair] = prefix or "0"
    else:
        assign_codes(node.left, prefix + "0", codes)
        assign_codes(node.right, prefix + "1", codes)

    return codes


def huffman_encode_pairs(text: str) -> str:
    """Кодирует текст, используя пары символов."""
    if len(text) < 2:
        return "0"  # Обработка коротких текстов

    freq_dict = build_pair_frequencies(text)
    tree = build_huffman_tree(freq_dict)
    codes = assign_codes(tree)

    # Разбиваем текст на пары
    pairs = [
        (text[i], text[i + 1])
        for i in range(0, len(text) - 1, 2)
    ]
    if len(text) % 2 != 0:
        pairs.append((text[-1], ""))  # Обработка нечётной длины

    encoded_bits = "".join(
        codes[pair]
        for pair in pairs
        if pair in codes
    )
    return encoded_bits
