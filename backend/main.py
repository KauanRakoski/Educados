from data_builder import DataFactory, Municipio, ListMunicipioOut, MunicipioOut, df_to_list, Trie, Trie_Node, Trie_Root
import os
import struct
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
from data_searcher import extract_municipios, extract_state


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
        'http://localhost:4200'
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

@app.get('/dados/RS', response_model = ListMunicipioOut)
def get_RS():
    return extract_state(0, r)

@app.get('/dados/SC', response_model = ListMunicipioOut)
def get_SC():
    return extract_state(1, r)

@app.get('/dados/PR', response_model = ListMunicipioOut)
def get_PR():
    return extract_state(2, r)

#@app.get('/estadual', response_model = ListMunicipioOut)
#def get_estadual():
#    pass

#@app.get('/publica', response_model = ListMunicipioOut)
#def get_publica():
#    pass

#@app.get('/federal', response_model = ListMunicipioOut)
#def get_federal():
#    pass


#inicio main
if __name__ == "__main__":

    r = Trie_Root()
    datafact = DataFactory()
    r = datafact.pipeline_to_file("data.csv")
    
#    path = os.path.join(os.path.dirname(__file__), "data.bin")
    
#    with open(path, "rb") as f:
#        while True:
#            buf = f.read(TOTAL_SIZE)
#            if not buf:
#                break
#            m = Municipio.get_bytes(buf)
#            print(m)
    uvicorn.run(app, host = "0.0.0.0", port = 5000)


#fim main
