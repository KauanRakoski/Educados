class Trie_Node:
    def __init__(self):
        self.is_word = False
        self.children = dict()
        self.offset = []      #There can be more than one town with the same name
    

class Trie:

    def __init__(self):
        self.root = Trie_Node()
    
    #given a string (Municipio's name) and its respective object offset (data.bin), inserts it into the TRIE
    def insert(self, word, offset):
        current_node = self.root

        for c in word:
            if c not in current_node.children:
                current_node.children[c] = Trie_Node()
            
            current_node = current_node.children[c]
        
        current_node.is_word = True
        current_node.offset.append(offset)
    
    #given a string (Municipio's name) returns its respective object offset (data.bin).
    #If the object does not exists, returns -1
    def search(self, word):
        current_node = self.root

        for c in word:
            if c not in current_node.children:
                return []
            current_node = current_node.children[c]

        if current_node.is_word:
            return current_node.offset
        return []
        
    def starts_with(self, prefix):
        words = []
        current_node = self.root

        for c in prefix:
            if c not in current_node.children:
                return words
            current_node = current_node.children[c]
        
        def _dfs(current_node, path):
            if current_node.is_word:
                words.append(''.join(path))

            for c, child_node in current_node.children.items():
                _dfs(child_node,path + [c])
        
        _dfs(current_node, list(prefix))

        return words
    
    def show_all(self):

        words = []

        def _dfs(current_node, path):
            if current_node.is_word:
                words.append(''.join(path))

            for c, child_node in current_node.children.items():
                _dfs(child_node,path + [c])
            
        _dfs(self.root, [])

        return words
    
    def show_all_offsets(self):
        offsets = []

        def _dfs(current_node):
            if current_node.is_word:
                offsets.extend(current_node.offset)  # adiciona todos os offsets da lista

            for _, child_node in current_node.children.items():
                _dfs(child_node)
    
        _dfs(self.root)

        return offsets
    
    def starts_with_offset(self, prefix):
        offsets = []
        current_node = self.root

        for c in prefix:
            if c not in current_node.children:
                return offsets 
            current_node = current_node.children[c]

        def _dfs(node):
            if node.is_word:
                offsets.extend(node.offset)
            for child in node.children.values():
                _dfs(child)

        _dfs(current_node)
        return offsets



class Trie_Root:
    def __init__(self):
        self.states = {0: Trie(), 1: Trie(), 2: Trie()} # 0 - RS, 1 - SC, - 2 PR


class MunicipioBTreeEntry:
    def __init__(self, cod_municipio: int, main_data_offset: int, saeb_data_offset: int):
        self.cod_municipio = cod_municipio
        self.main_data_offset: int = main_data_offset
        self.saeb_data_offset: int = saeb_data_offset

    def __repr__(self):
        return f"MunicipioBTreeEntry(cod={self.cod_municipio}, main_offset={self.main_data_offset}, saeb_offset={self.saeb_data_offset})"