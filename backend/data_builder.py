import pandas as pd
from pandas import DataFrame
from dataclasses import dataclass
import struct

PACK_STR = 'i50siiffff'
PACK_SIZE = struct.calcsize(PACK_STR)

@dataclass
class Municipio:
    cod_municipio: int
    nome: str
    estado: int # 0 - RS 1 - SC 2 - PR
    rede: int # 0 - pública, 1 - estadual, 2 - federal
    ideb2017: float
    ideb2019: float
    ideb2021: float
    ideb2023: float
    
    def to_bytes(self) -> bytes:
        """converts a struct to bytes to be stored"""
        nome_b = self.nome.encode("utf-8")[:50]
        nome_b = nome_b.ljust(50, b"\x00")

        return struct.pack(
            PACK_STR,
            self.cod_municipio,
            nome_b,
            self.estado,
            self.rede,
            self.ideb2017,
            self.ideb2019,
            self.ideb2021,
            self.ideb2023
            )
    
    @classmethod
    def get_bytes(self, b: bytes):
        """Returns a struct from binary data"""
        cod_municipio, nome_b, estado, rede, ideb2017, ideb2019, ideb2021, ideb2023 = struct.unpack(PACK_STR, b)
        nome   = nome_b.rstrip(b"\x00").decode("utf-8")
        return self(cod_municipio, nome, estado, rede, ideb2017, ideb2019, ideb2021, ideb2023)

class DataFactory:
    data = pd.DataFrame()
    
    def load_csv(self, csv_path: str) -> None:
        """Loads a dataframe based on a csv"""
        self.data = pd.read_csv(csv_path)
    
    def filter_by_states (self, states: list) -> None:
        """Given a list of states, filters the dataframe"""
        for state in states:
            self.data = self.data[self.data['SG_UF'] == state]
            
    def _state_value (self, state: str) -> int:
        if state == "RS":
            return 0
        if state == "SC":
            return 1
        
        return 2

    def _rede_value (self, rede: str) -> int:
        if rede == "Pública":
            return 0
        if rede == "Estadual":
            return 1
        
        return 2

    def pipeline_to_file(self, path_to_file: str) -> None:
        self.load_csv(path_to_file)
        self.filter_by_states(['RS', 'SC', 'PR'])
        
        for row in self.data.itertuples(index=False):
            m = Municipio(
                cod_municipio= row.COD_MUNICIPIO,
                nome = row.NOME_MUNICIPIO,
                estado = self._state_value(row.SG_UF),
                rede = self._rede_value(row.REDE),
                ideb2017=float(row.IDEB_2017),
                ideb2019=float(row.IDEB_2019),
                ideb2021=float(row.IDEB_2021),
                ideb2023=float(row.IDEB_2023)
            )
            
            with open('data.bin', 'wb') as f:
                f.write(m.to_bytes())
        
        