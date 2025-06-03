from data_builder import DataFactory, Municipio
import os
import struct
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

PACK_STR = 'i50si'
PACK_SIZE = struct.calcsize(PACK_STR)

REDE_PACK_STR = 'iffff'
REDE_PACK_SIZE = struct.calcsize(REDE_PACK_STR)

NUM_REDES = 3
TOTAL_SIZE = PACK_SIZE + (NUM_REDES * REDE_PACK_SIZE)

def main():
    datafact = DataFactory()
    datafact.pipeline_to_file("data.csv")
    
    path = os.path.join(os.path.dirname(__file__), "data.bin")
    
    with open(path, "rb") as f:
        while True:
            buf = f.read(TOTAL_SIZE)
            if not buf:
                break
            m = Municipio.get_bytes(buf)
            print(m)
            
if __name__ == "__main__":
    main()