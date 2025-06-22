from data_builder import DataFactory, Municipio, ListMunicipioOut, MunicipioOut, df_to_list, Trie, Trie_Node, Trie_Root
import os
import struct
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from data_searcher import extract_municipios, extract_state, extract_town_by_name, extract_state_name


PACK_STR = 'i50si'
PACK_SIZE = struct.calcsize(PACK_STR)

REDE_PACK_STR = 'iffff'
REDE_PACK_SIZE = struct.calcsize(REDE_PACK_STR)

NUM_REDES = 3

#Absolute size of a Municipio Entity in data.bin
TOTAL_SIZE = PACK_SIZE + (NUM_REDES * REDE_PACK_SIZE)

app = FastAPI()

origins = [
        #Insert the URL of the frontend server
        'http://localhost:4200',
        'http://localhost:5000'
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


@app.get('/dados', response_model = ListMunicipioOut)
def get_data(state: Optional[str] = None, name: Optional[str] = None):
    if state is None or state == "":
        if name is None or name == "":
            return extract_municipios()
        return extract_town_by_name(r, name)
    
    if state == 'RS':
        status = 0
    elif state == 'SC':
        status = 1
    else:
        status = 2

    if name is None or name == "":
        return extract_state(status, r)
    return extract_state_name(r, name, status)
    
    
if __name__ == "__main__":

    r = Trie_Root()
    datafact = DataFactory()
    r = datafact.pipeline_to_file("data.csv")
    
    uvicorn.run(app, host = "0.0.0.0", port = 5000)
