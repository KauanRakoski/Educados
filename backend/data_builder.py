import pandas as pd
from pandas import DataFrame
from dataclasses import dataclass
import struct
from pydantic import BaseModel
from typing import List
import os
from BTrees.OOBTree import OOBTree
import pickle

PACK_STR = 'i50si'
PACK_SIZE = struct.calcsize(PACK_STR)

REDE_PACK_STR = 'iffff'
REDE_PACK_SIZE = struct.calcsize(REDE_PACK_STR)

NUM_REDES = 3
REDE_PUBLICA = 0
REDE_ESTADUAL = 1
REDE_FEDERAL = 2

#Absolute size of a Municipio Entity in data.bin
TOTAL_SIZE = PACK_SIZE + (NUM_REDES * REDE_PACK_SIZE)

#OLD DEFINITION
#class RedesOut(BaseModel):
#    rede: str
#    ideb2017: float
#    ideb2019: float
#    ideb2021: float
#    ideb2023: float

CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzáàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ -'
CHAR_TO_INDEX = {c: i for i, c in enumerate(CHARSET)}
INDEX_TO_CHAR = {i: c for i, c in enumerate(CHARSET)}
MAX_CHILDREN = len(CHARSET)
MAX_OFFSETS = 3  # número fixo de offsets
NODE_SIZE = 1 + 4 * MAX_OFFSETS + 4 * MAX_CHILDREN  # total em bytes por nó

#NEW DEFINITION
class RedesOut(BaseModel):
    rede: int
    ideb2017: float
    ideb2019: float
    ideb2021: float
    ideb2023: float
class MunicipioOut(BaseModel):
    cod_municipio: int
    nome: str
    estado: str
    redes: List[RedesOut]

class ListMunicipioOut(BaseModel):
    municipios: List[MunicipioOut]

@dataclass
class Rede:
    rede: int
    ideb2017: float
    ideb2019: float
    ideb2021: float
    ideb2023: float
    
    def to_bytes(self):
        """converts a struct to bytes to be stored"""
        return struct.pack(
            REDE_PACK_STR,
            self.rede,
            self.ideb2017,
            self.ideb2019,
            self.ideb2021,
            self.ideb2023
        )
    
    @classmethod
    def get_bytes(cls, b: bytes):
        """Returns a struct from binary data"""
        rede, ideb2017, ideb2019, ideb2021, ideb2023 = struct.unpack(REDE_PACK_STR, b)
        return cls(rede, ideb2017, ideb2019, ideb2021, ideb2023)
    
    @classmethod
    def empty(cls):
        return cls(rede=-1, ideb2017=0.0, ideb2019=0.0, ideb2021=0.0, ideb2023=0.0)
    
    
@dataclass
class Municipio:
    cod_municipio: int
    nome: str
    estado: int # 0 - RS 1 - SC 2 - PR
    redes: list[Rede]
    
    def to_bytes(self) -> bytes:
        """converts a struct to bytes to be stored"""
        nome_b = self.nome.encode("utf-8")[:50]
        nome_b = nome_b.ljust(50, b"\x00")

        header = struct.pack(
            PACK_STR,
            self.cod_municipio,
            nome_b,
            self.estado,
            )
        
        redes_bytes = b''
        
        for i in range (NUM_REDES):
            rede_add = None
            
            for rede_data in self.redes:
                if rede_data.rede == i:
                    rede_add = rede_data
                    break
            
            if rede_add:
                redes_bytes += rede_add.to_bytes()
            else:
                redes_bytes += Rede.empty().to_bytes()
                    
        return header + redes_bytes
    
    @classmethod
    def get_bytes(cls, b: bytes):
        """Returns a municipio struct from binary data"""
        header_bytes = b[:PACK_SIZE]
        cod_municipio, nome_b, estado = struct.unpack(PACK_STR, header_bytes)
        nome = nome_b.rstrip(b"\x00").decode("utf-8")

        redes_data = []
        offset = PACK_SIZE
        
        for _ in range(NUM_REDES):
            rede_bytes = b[offset : offset + REDE_PACK_SIZE]
            redes_data.append(Rede.get_bytes(rede_bytes))
            offset += REDE_PACK_SIZE

        return cls(cod_municipio, nome, estado, redes_data)
    

class DataFactory:
    data = pd.DataFrame()
    
    def load_csv(self, csv_path: str) -> None:
        """Loads a dataframe based on a csv"""
        self.data = pd.read_csv(csv_path)
    
    def filter_by_states (self, states: list) -> None:
        """Given a list of states, filters the dataframe"""
        self.data = self.data[self.data['SG_UF'].isin(states)]
            
    def _state_value (self, state: str) -> int:
        if state == "RS":
            return 0
        if state == "SC":
            return 1
        
        return 2

    def _rede_value (self, rede: str) -> int:
        if rede == "Pública":
            return REDE_PUBLICA
        if rede == "Estadual":
            return REDE_ESTADUAL
        
        return REDE_FEDERAL

    def ideb_value (self, value_str: str) -> float:
        if value_str != '-':
            return float(value_str)
        return 0
        
    def pipeline_to_file(self, path_to_file: str):
        """
        Loads csv data into a dataframe, applies the necessary filters and aggregates the data.
        Writes the result to a binary file
        """
        
        self.load_csv(path_to_file)
        self.filter_by_states(['RS', 'SC', 'PR'])
        
        # print(self.data.columns)
        grouped_data = self.data.groupby(['COD_MUNICIPIO'])
        # Iterate through groups and print
        
        with open('data2.bin', 'wb') as f:
            
            counter = 0
            prefix_root_tree = Trie_Root()
            btree = OOBTree() #Criamos uma Btree
            

            for _, group_df in grouped_data:
                sg_uf = group_df['SG_UF'].iloc[0]
                cod_municipio = group_df['COD_MUNICIPIO'].iloc[0]
                nome_municipio = group_df['NOME_MUNICIPIO'].iloc[0]

                mun_btree = MunicipioBTreeEntry(cod_municipio)
                # dentro do loop do grupo
                rede_publica = RedeData(REDE_PUBLICA)
                rede_estadual = RedeData(REDE_ESTADUAL)
                rede_federal = RedeData(REDE_FEDERAL)

                
                redes_data: list[Rede] = []
                
                # map which rede exists
                existing_rede = {REDE_PUBLICA: None, REDE_ESTADUAL: None, REDE_FEDERAL: None}
                
                for _, row in group_df.iterrows():
                    
                    rede_type = self._rede_value(row['REDE'])
                    
                    rede = Rede(
                        rede=rede_type,
                        ideb2017=self.ideb_value(row['IDEB_2017']),
                        ideb2019=self.ideb_value(row['IDEB_2019']),
                        ideb2021=self.ideb_value(row['IDEB_2021']),
                        ideb2023=self.ideb_value(row['IDEB_2023'])
                    )
                    
                    existing_rede[rede_type] = rede

                    if rede_type == REDE_PUBLICA:
                        rede_publica.set_ideb(2017, rede.ideb2017)
                        rede_publica.set_ideb(2019, rede.ideb2019)
                        rede_publica.set_ideb(2021, rede.ideb2021)
                        rede_publica.set_ideb(2023, rede.ideb2023)

                        rede_publica.set_saeb(2017, math = row['SAEB_MAT_2017'], port = row['SAEB_PORT_2017'], final_grade = row['SAEB_NOTA_2017'])
                        rede_publica.set_saeb(2019, math = row['SAEB_MAT_2019'], port = row['SAEB_PORT_2019'], final_grade = row['SAEB_NOTA_2019'])
                        rede_publica.set_saeb(2021, math = row['SAEB_MAT_2021'], port = row['SAEB_PORT_2021'], final_grade = row['SAEB_NOTA_2021'])
                        rede_publica.set_saeb(2023, math = row['SAEB_MAT_2023'], port = row['SAEB_PORT_2023'], final_grade = row['SAEB_NOTA_2023'])
                    elif rede_type == REDE_ESTADUAL:
                        rede_estadual.set_ideb(2017, rede.ideb2017)
                        rede_estadual.set_ideb(2019, rede.ideb2019)
                        rede_estadual.set_ideb(2021, rede.ideb2021)
                        rede_estadual.set_ideb(2023, rede.ideb2023)

                        rede_estadual.set_saeb(2017, math = row['SAEB_MAT_2017'], port = row['SAEB_PORT_2017'], final_grade = row['SAEB_NOTA_2017'])
                        rede_estadual.set_saeb(2019, math = row['SAEB_MAT_2019'], port = row['SAEB_PORT_2019'], final_grade = row['SAEB_NOTA_2019'])
                        rede_estadual.set_saeb(2021, math = row['SAEB_MAT_2021'], port = row['SAEB_PORT_2021'], final_grade = row['SAEB_NOTA_2021'])
                        rede_estadual.set_saeb(2023, math = row['SAEB_MAT_2023'], port = row['SAEB_PORT_2023'], final_grade = row['SAEB_NOTA_2023'])
                    else:
                        rede_federal.set_ideb(2017, rede.ideb2017)
                        rede_federal.set_ideb(2019, rede.ideb2019)
                        rede_federal.set_ideb(2021, rede.ideb2021)
                        rede_federal.set_ideb(2023, rede.ideb2023)

                        rede_federal.set_saeb(2017, math = row['SAEB_MAT_2017'], port = row['SAEB_PORT_2017'], final_grade = row['SAEB_NOTA_2017'])
                        rede_federal.set_saeb(2019, math = row['SAEB_MAT_2019'], port = row['SAEB_PORT_2019'], final_grade = row['SAEB_NOTA_2019'])
                        rede_federal.set_saeb(2021, math = row['SAEB_MAT_2021'], port = row['SAEB_PORT_2021'], final_grade = row['SAEB_NOTA_2021'])
                        rede_federal.set_saeb(2023, math = row['SAEB_MAT_2023'], port = row['SAEB_PORT_2023'], final_grade = row['SAEB_NOTA_2023'])

                    
                    for i in range(NUM_REDES):
                        if existing_rede[i]:
                            redes_data.append(existing_rede[i])
                        else:
                            redes_data.append(Rede.empty())
                            
                m = Municipio(
                    cod_municipio=cod_municipio,
                    nome=nome_municipio,
                    estado=self._state_value(sg_uf),
                    redes=redes_data 
                )
            
                f.write(m.to_bytes())
                prefix_root_tree.states[self._state_value(sg_uf)].insert(nome_municipio, (counter  * TOTAL_SIZE))
                counter = counter + 1

                mun_btree.add_rede(rede_publica)
                mun_btree.add_rede(rede_estadual)
                mun_btree.add_rede(rede_federal)

                btree[cod_municipio] = mun_btree

            return btree
        
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


class SaebGrades:
    def __init__(self, math: float, port: float, final_grade: float):
        self.math = math
        self.port = port
        self.final_grade = final_grade

    def __repr__(self):
        return f"SaebGrades(math={self.math}, port={self.port}, final={self.final_grade})"

class RedeData:
    def __init__(self, rede: int):
        self.rede = rede
        self.ideb = {
            2017: None,
            2019: None,
            2021: None,
            2023: None,
        }
        self.saeb = {
            2017: None,
            2019: None,
            2021: None,
            2023: None,
        }

    def set_ideb(self, year: int, grade: float):
        if year in self.ideb:
            self.ideb[year] = grade

    def set_saeb(self, year: int, math: float, port: float, final_grade: float):
        if year in self.saeb:
            self.saeb[year] = SaebGrades(math, port, final_grade)
    
    def __repr__(self):
        return f"RedeData(rede={self.rede}, ideb={self.ideb}, saeb={self.saeb})"

class MunicipioBTreeEntry:
    def __init__(self, cod_municipio: int):
        self.cod_municipio = cod_municipio
        self.redes: list[RedeData] = []

    def add_rede(self, rede: RedeData):
        self.redes.append(rede)

    def __repr__(self):
        return f"MunicipioBTreeEntry(cod={self.cod_municipio}, redes={self.redes})"

def save_trie_root(r: Trie_Root):
    with open("trie.bin", "wb") as f:
        pickle.dump(r, f)

def load_trie_root():
    with open("trie.bin", "rb") as f:
        return pickle.load(f)
    
def save_btree(b: OOBTree):
    with open("btree.bin", "wb") as f:
        pickle.dump(b, f)

def load_btree():
    with open("btree.bin", "rb") as f:
        return pickle.load(f)