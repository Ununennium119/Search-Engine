import time
from typing import Optional, Dict, List


def main():
    build_tries()

    start_time = time.time()
    search_docs()
    end_time = time.time()
    duration = (end_time - start_time) / 1_000_000

    time_file = open("time.txt", mode='w')
    time_file.write(str(duration))
    time_file.close()
    print(duration)


class DocCount:
    def __init__(self, doc_index: int, count: int):
        self.doc_index: int = doc_index
        self.count: int = count


class Dictionary:
    def __init__(self):
        self.dict: dict = dict()


class TrieNode:
    def __init__(self):
        self.children: List[Optional[TrieNode]] = [None] * 26
        self.is_end_of_word: int = 0


class Trie:
    def __init__(self, is_reversed: bool):
        self.root: TrieNode = TrieNode()
        self.is_reversed: bool = is_reversed
        self.size: int = 0

    @staticmethod
    def _letter_to_index(letter: str) -> int:
        """Return ascii code of lowered letter mapped to 0 to 26

        Return -1 if letter is not a-z or A-Z
        """
        letter_ascii: int = ord(letter)
        if 65 <= letter_ascii <= 90:
            return letter_ascii - 65
        elif 97 <= letter_ascii <= 122:
            return letter_ascii - 97
        else:
            return -1

    @staticmethod
    def _index_to_letter(n: int) -> str:
        """return (n + 1)th letter in alphabet"""
        return chr(n + 97)

    def _get_loop_range(self, word: str) -> range:
        """Return the order to visit word letters"""
        if self.is_reversed:
            return range(len(word) - 1, -1, -1)
        else:
            return range(len(word))

    def insert(self, word: str):
        """Insert word into trie"""
        current_node: TrieNode = self.root
        for i in self._get_loop_range(word):
            letter = word[i]
            index = Trie._letter_to_index(letter)
            if index == -1:
                continue
            if current_node.children[index] is None:
                current_node.children[index] = TrieNode()
            current_node = current_node.children[index]
        current_node.is_end_of_word += 1
        self.size += 1

    def search_pattern(self, pattern: str) -> Dict[str, int]:
        """Return words start with the prefix in the trie"""
        current_node: TrieNode = self.root
        for i in self._get_loop_range(pattern):
            letter = pattern[i]
            index = Trie._letter_to_index(letter)
            if current_node.children[index] is None:
                return dict()
            current_node = current_node.children[index]
        matched_words = Dictionary()
        self.traverse_subtree(current_node, pattern, matched_words)
        return matched_words.dict

    def traverse_subtree(self, subtree_root: TrieNode, root_value: str, words: Dictionary):
        """Return all words in subtree"""
        if subtree_root.is_end_of_word > 0:
            words.dict[root_value] = subtree_root.is_end_of_word
        for i, child in enumerate(subtree_root.children):
            if child is not None:
                if self.is_reversed:
                    new_root_value = Trie._index_to_letter(i) + root_value
                else:
                    new_root_value = root_value + Trie._index_to_letter(i)
                self.traverse_subtree(child, new_root_value, words)


docs_tries: List[Trie] = []
docs_reversed_tries: List[Trie] = []


def search_docs():
    input_file = open("input.txt", mode='r')
    result_file = open("result.txt", mode='w')
    queries_count = int(input_file.readline())
    queries: List[str] = input_file.read().splitlines()
    for pattern in queries:
        prefix, suffix = pattern.split("\\S*")
        matched_words_counts: List[DocCount] = []
        for j in range(10):
            if len(prefix) == 0 and len(suffix) == 0:
                matched_words_counts.append(DocCount(j + 1, docs_tries[j].size))
            elif len(prefix) == 0:
                matched_words = docs_reversed_tries[j].search_pattern(suffix)
                matched_words_counts.append(DocCount(j + 1, sum(matched_words.values())))
            elif len(suffix) == 0:
                matched_words = docs_tries[j].search_pattern(prefix)
                matched_words_counts.append(DocCount(j + 1, sum(matched_words.values())))
            else:
                prefix_matched_words = docs_tries[j].search_pattern(prefix)
                suffix_matched_words = docs_reversed_tries[j].search_pattern(suffix)

                pattern_len = len(prefix) + len(suffix)
                shared_keys = prefix_matched_words.keys() & suffix_matched_words.keys()
                matched_words_count = 0
                for key in shared_keys:
                    if len(key) >= pattern_len:
                        matched_words_count += prefix_matched_words[key]
                matched_words_counts.append(DocCount(j + 1, matched_words_count))
        matched_words_counts.sort(key=lambda item: (item.count, -item.doc_index), reverse=True)
        if all(item.count == 0 for item in matched_words_counts):
            result_file.write("-1\n")
        else:
            result_file.write(f"{' '.join([str(item.doc_index) for item in matched_words_counts if item.count > 0])}\n")
    input_file.close()


def build_tries():
    for i in range(10):
        doc = open(f"doc{i + 1:02}.txt", mode='r', encoding="utf8")
        trie = Trie(False)
        reversed_trie = Trie(True)
        for word in doc.readline().split(' '):
            trie.insert(word)
            reversed_trie.insert(word)
        docs_tries.append(trie)
        docs_reversed_tries.append(reversed_trie)
        doc.close()


if __name__ == '__main__':
    main()
