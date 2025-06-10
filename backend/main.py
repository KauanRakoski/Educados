from data_builder import DataFactory, Municipio, ListMunicipioOut, MunicipioOut, df_to_list
import os
import struct
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
from data_searcher import extract_municipios

PACK_STR = 'i50si'
PACK_SIZE = struct.calcsize(PACK_STR)

REDE_PACK_STR = 'iffff'
REDE_PACK_SIZE = struct.calcsize(REDE_PACK_STR)

NUM_REDES = 3

#Absolute size of a Municipio Entity in data.bin
TOTAL_SIZE = PACK_SIZE + (NUM_REDES * REDE_PACK_SIZE)



#class ListMunicipioOut(BaseModel):
    
#    municipios = List[MunicipioOut]

#    def __init__(self, municipio: MunicipioOut):
#        self.municipios = municipio

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

#@app.get("/dados", response_model = ListMunicipioOut)
#def get_towns():
#    return ListMunicipioOut(municipios = df_to_list(datafact.data))

@app.get("/dados", response_model = ListMunicipioOut)
def get_towns():
    return extract_municipios()

#inicio main
if __name__ == "__main__":

    datafact = DataFactory()
    datafact.pipeline_to_file("data.csv")
    
#    path = os.path.join(os.path.dirname(__file__), "data.bin")
    
#    with open(path, "rb") as f:
#        while True:
#            buf = f.read(TOTAL_SIZE)
#            if not buf:
#                break
#            m = Municipio.get_bytes(buf)
#            print(m)
    uvicorn.run(app, host = "0.0.0.0", port = 5000)

    #lista_mun = ListMunicipioOut(municipios = [])
    #lista_mun = extract_municipios()
    #print(lista_mun.municipios)


#fim main
