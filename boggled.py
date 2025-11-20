from typing import List, Tuple, Set, Dict

class TrieNode:
    def __init__(self, letter=None) -> None:
        self.letter = letter
        self.end:bool = False
        self.pointers: Dict[str, TrieNode] = {}
        # add attributes for whether it is the end of a word and a collection of pointers to
        # next letters

class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def generate_tree_from_file(self)->None:
        words = self._load_words()
        #add code here to set up the TrieNode tree structure for the words
        for word in words:
            self.insert(word)
    
    def insert (self, word:str) -> None:
        current = self.root
        for letter in reversed(word):
            if letter not in current.pointers:
                current.pointers[letter] = TrieNode(letter)
            current = current.pointers[letter]
        current.end = True
                    

    # helper to load words. No modifications needed
    def _load_words(self):
        words = []
        with open("words.txt", "r", encoding="utf-8") as file:
            for line in file:
                word = line.strip()
                words.append(word)
        return words

# Implement the Boggled Solver. This Boggle has the following special properties:
# 1) All words returned should end in a specified suffix (i.e. encode the trie in reverse)
# 2) Board tiles may have more than 1 letter (e.g. "qu" or "an")
# 3) The number of times you can use the same tile in a word is variable
# Your implementation should account for all these properties.
class Boggled:

    def __init__(self):
        self.trie = Trie()

    # setup test initializes the game with the game board and the max number of times we can use each 
    # tile per word
    def setup_board(self, max_uses_per_tile: int, board:List[List[str]])->None:
        self.max_uses_per_tile = max_uses_per_tile
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0]) 
        self.directions:List[tuple] = [(-1,0), (0,-1), (-1,-1), (0,1), (1,0), (1,1), (-1,1), (1,-1)]
        self.trie.generate_tree_from_file()

    
    # Returns a set of all words on the Boggle board that end in the suffix parameter string. Words can be found
    # in all 8 directions from a position on the board
    def get_all_words(self, suffix:str)->Set:
        found_words = set()
        for r in range(self.rows):
            for c in range(self.cols):
                self.get_all_words_recursive(r, c, self.trie.root, "", found_words, {}, suffix)       
        return found_words

    # recursive helper for get_all_words. Customize parameters as needed; you will likely need params for 
    # at least a board position and tile
    def get_all_words_recursive(self, r: int, c: int, node: TrieNode, path: str, found_words: Set[str], used_tiles: Dict[Tuple[int, int], int], suffix: str):
        if r < 0 or c < 0 or r >= self.rows or c >= self.cols:
            return
        
        tile = self.board[r][c]
        new_path = tile + path  

        #  max usage of tiles
        new_used_tiles = used_tiles.copy()
        new_used_tiles[(r, c)] = new_used_tiles.get((r, c), 0) + 1
        if new_used_tiles[(r, c)] > self.max_uses_per_tile:
            return

        # Traverse the Trie
        temp_node = node
        for letter in reversed(tile):  
            if letter in temp_node.pointers:
                temp_node = temp_node.pointers[letter]
            else:
                return
            
           # valid suffix match
        if not(suffix.endswith(new_path) or new_path.endswith(suffix)):
            return

        # Check if we found a valid word
        if temp_node.end and len(new_path) > len(suffix):
            found_words.add(new_path)

        # Continue searching in all directions
        for dr, dc in self.directions:
            self.get_all_words_recursive(r + dr, c + dc, temp_node, new_path, found_words, new_used_tiles, suffix)
