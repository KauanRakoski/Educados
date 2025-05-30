from data_builder import DataFactory, Municipio
import os
import struct

RECORD_FORMAT = 'i50s2s'
RECORD_SIZE = struct.calcsize(RECORD_FORMAT)

def main():
    datafact = DataFactory()
    datafact.pipeline_to_file("data.csv")
    
    path = os.path.join(os.path.dirname(__file__), "data.bin")
    
    with open(path, "rb") as f:
        while True:
            buf = f.read(RECORD_SIZE)
            if not buf:
                break
            m = Municipio.from_bytes(buf)
            print(m)
            
if __name__ == "__main__":
    main()