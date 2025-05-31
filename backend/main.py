from data_builder import DataFactory, Municipio
import os
import struct

PACK_STR = 'i50siiffff'
PACK_SIZE = struct.calcsize(PACK_STR)

def main():
    datafact = DataFactory()
    datafact.pipeline_to_file("data.csv")
    
    path = os.path.join(os.path.dirname(__file__), "data.bin")
    
    with open(path, "rb") as f:
        while True:
            buf = f.read(PACK_SIZE)
            if not buf:
                break
            m = Municipio.get_bytes(buf)
            print(m)
            
if __name__ == "__main__":
    main()