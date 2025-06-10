import pandas as pd
from pandas import DataFrame
from dataclasses import dataclass
import struct
from pydantic import BaseModel
from typing import List

PACK_STR = 'i50si'
PACK_SIZE = struct.calcsize(PACK_STR)

REDE_PACK_STR = 'iffff'
REDE_PACK_SIZE = struct.calcsize(REDE_PACK_STR)

NUM_REDES = 3
REDE_PUBLICA = 0
REDE_ESTADUAL = 1
REDE_FEDERAL = 2


#OLD DEFINITION
#class RedesOut(BaseModel):
#    rede: str
#    ideb2017: float
#    ideb2019: float
#    ideb2021: float
#    ideb2023: float

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
    

class Trie_Node:
    def __init__(self):
        is_word = False
        self.children = dict()
        self.offset = int()
    

class Trie:

    def __init__(self):
        root = Trie_Node()
    
    #given a string (Municipio's name) and its respective object offset (data.bin), inserts it into the TRIE
    def insert(self, word, offset):
        current_node = self.root

        for c in word:
            if c in current_node.children:
                current_node.children[c] = Trie_Node()
            
            current_node = current_node.children[c]
        
        current_node.is_word = True
        current_node.offset = offset
    
    #given a string (Municipio's name) returns its respective object offset (data.bin).
    #If the object does not exists, returns -1
    def search(self, word):
        current_node = self.root

        for c in word:
            if c not in current_node.children:
                return -1
            current_node = current_node.children[c]

        return current_node.offset
    

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
        
    def pipeline_to_file(self, path_to_file: str) -> None:
        """
        Loads csv data into a dataframe, applies the necessary filters and aggregates the data.
        Writes the result to a binary file
        """
        
        self.load_csv(path_to_file)
        self.filter_by_states(['RS', 'SC', 'PR'])
        
        # print(self.data.columns)
        grouped_data = self.data.groupby(['COD_MUNICIPIO'])
        # Iterate through groups and print
        
        with open('data.bin', 'wb') as f:
            for _, group_df in grouped_data:
                sg_uf = group_df['SG_UF'].iloc[0]
                cod_municipio = group_df['COD_MUNICIPIO'].iloc[0]
                nome_municipio = group_df['NOME_MUNICIPIO'].iloc[0]
                
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


#Takes a dataframe as input and returns a list of MunicipiosOut (POR FAZER)
def df_to_list(datafr) -> List[MunicipioOut]:

    estados_map = {"RS": 0, "SC": 1, "PR": 2}

    municipios_dict = {}

    for _,row in datafr.iterrows():
        cod_mun = row['COD_MUNICIPIO']

        if cod_mun  not in municipios_dict:
            mun = MunicipioOut(
                cod_municipio = cod_mun,
                nome = row['NOME_MUNICIPIO'],
                estado = row['SG_UF'],
                redes = []
            )

        municipios_dict[cod_mun] = mun

        id17 = -1
        id19 = -1
        id21 = -1
        id23 = -1

        if row['IDEB_2017'] != '-':
            id17 = float(row['IDEB_2017'])
        if row['IDEB_2019'] != '-':
            id19 = float(row['IDEB_2019'])
        if row['IDEB_2021'] != '-':
            id21 = float(row['IDEB_2021'])
        if row['IDEB_2023'] != '-':
            id23 = float(row['IDEB_2023'])
       
        rede_obj = RedesOut(
            rede = row['REDE'],
            ideb2017 = id17,
            ideb2019 = id19,
            ideb2021 = id21,
            ideb2023 = id23
        )

        municipios_dict[cod_mun].redes.append(rede_obj)

    return list(municipios_dict.values())