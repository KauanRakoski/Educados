from data_builder import DataFactory, Municipio
import os
import struct
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn

PACK_STR = 'i50si'
PACK_SIZE = struct.calcsize(PACK_STR)

REDE_PACK_STR = 'iffff'
REDE_PACK_SIZE = struct.calcsize(REDE_PACK_STR)

NUM_REDES = 3

#Absolute size of a Municipio Entity in data.bin
TOTAL_SIZE = PACK_SIZE + (NUM_REDES * REDE_PACK_SIZE)

class RedesOut(BaseModel):
    rede: str
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



app = FastAPI()

origins = [
        #Insert the URL of the frontend server
        'http://localhost:5000'
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


@app.get("/", response_model = ListMunicipioOut)
def get_towns():
    return ListMunicipioOut(municipios = df_to_list(datafact.data))


#inicio main
if __name__ == "__main__":

    datafact = DataFactory()
    datafact.pipeline_to_file("data.csv")
    
    path = os.path.join(os.path.dirname(__file__), "data.bin")
    
    with open(path, "rb") as f:
        while True:
            buf = f.read(TOTAL_SIZE)
            if not buf:
                break
            m = Municipio.get_bytes(buf)
            #print(m)
    uvicorn.run(app, host = "0.0.0.0", port = 5000)
#fim main
