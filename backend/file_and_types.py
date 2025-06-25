from dataclasses import dataclass
import struct
import pickle
from pydantic import BaseModel
from BTrees.OOBTree import OOBTree
from typing import List
from trees import *

PACK_STR = 'i50si'
PACK_SIZE = struct.calcsize(PACK_STR)

REDE_PACK_STR = 'iffff'
REDE_PACK_SIZE = struct.calcsize(REDE_PACK_STR)

NUM_REDES = 3
REDE_PUBLICA = 0
REDE_ESTADUAL = 1
REDE_FEDERAL = 2

#Absolute size of a Municipio Entity in data.bin (used for offset calc)
TOTAL_SIZE = PACK_SIZE + (NUM_REDES * REDE_PACK_SIZE)

# +++++++++++++++++++++++++++++++++++++++
# +          BASE TYPES                 +
# +++++++++++++++++++++++++++++++++++++++
"""
Each Municipio posesses 1 to 3 Redes.
Each Rede posesses up to 4 IDEBS and 4 saebs
Each SAEB has portuguese, math and final grades

In SAEB.bin we need only to adress for each town the code and saebs for each rede
"""
class SaebNotas:
    def __init__(self, math: float, port: float, final: float):
        self.math = math
        self.port = port
        self.final = final

    def __repr__(self):
        return f"SaebNotas(math={self.math}, port={self.port}, final={self.final})"


class RedeSaeb:
    def __init__(self, codigo_rede: int):
        self.codigo_rede = codigo_rede
        # até 4 edições do SAEB (anos)
        self.saeb = {
            2017: None,
            2019: None,
            2021: None,
            2023: None,
        }

    def set_saeb(self, ano: int, math: float, port: float, final: float):
        if ano in self.saeb:
            self.saeb[ano] = SaebNotas(math, port, final)

    def __repr__(self):
        return f"RedeSaeb(codigo_rede={self.codigo_rede}, saeb={self.saeb})"


class MunicipioSaeb:
    def __init__(self, cod_municipio: int):
        self.cod_municipio = cod_municipio
        # até 3 redes por município
        self.redes = {}  # mapa codigo_rede → RedeSaeb

    def add_rede(self, codigo_rede: int):
        if len(self.redes) < 3 and codigo_rede not in self.redes:
            self.redes[codigo_rede] = RedeSaeb(codigo_rede)

    def get_rede(self, codigo_rede: int) -> RedeSaeb:
        return self.redes.get(codigo_rede)

    def __repr__(self):
        return f"MunicipioSaeb(cod_municipio={self.cod_municipio}, redes={self.redes})"
    


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
    
    
  
    
    
# +++++++++++++++++++++++++++++++++++++
# +   CLASSES FOR MUNICIPIO DATA      +
# +++++++++++++++++++++++++++++++++++++

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
    

# +++++++++++++++++++++++++
# +      FILE METHODS     +
# +++++++++++++++++++++++++

class TreeHandler():
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