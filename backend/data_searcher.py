from data_builder import DataFactory, Municipio, ListMunicipioOut, MunicipioOut, df_to_list, RedesOut, Trie_Root
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


#reads data.bin and stores the Municipios objects in the list of a ListMunicipioOut object
def extract_municipios() -> ListMunicipioOut:

    lista_municipios = ListMunicipioOut(municipios = [])

    path = os.path.join(os.path.dirname(__file__), "data.bin")

    with open(path, "rb") as f:
        while True:
            buf = f.read(TOTAL_SIZE)
            if not buf:
                break
            m = Municipio.get_bytes(buf)

            if m.estado == 0:
                state_value = 'RS'
            elif m.estado == 1:
                state_value = 'SC'
            else:
                state_value = 'PR'

            list_redes: list[RedesOut] = []


            for j in range(NUM_REDES):

                r = RedesOut(
                    rede = m.redes[j].rede, #mudar para string se necessário
                    ideb2017 = m.redes[j].ideb2017,
                    ideb2019 = m.redes[j].ideb2019,
                    ideb2021 = m.redes[j].ideb2021,
                    ideb2023 = m.redes[j].ideb2023
                )

                list_redes.append(r)

            munout = MunicipioOut(
                cod_municipio = m.cod_municipio,
                nome = m.nome,
                estado = state_value,
                redes = list_redes
            )

            lista_municipios.municipios.append(munout)

    return lista_municipios


def extract_state(state: int, r: Trie_Root) -> ListMunicipioOut:
    
    offsets = r.states[state].show_all_offsets()
    lista_municipios = ListMunicipioOut(municipios = [])

    path = os.path.join(os.path.dirname(__file__), "data.bin")

    with open(path, "rb") as f:
        for i in offsets:
            f.seek(i)
            buf = f.read(TOTAL_SIZE)
            if not buf:
                break
            m = Municipio.get_bytes(buf)

            if m.estado == 0:
                state_value = 'RS'
            elif m.estado == 1:
                state_value = 'SC'
            else:
                state_value = 'PR'

            list_redes: list[RedesOut] = []


            for j in range(NUM_REDES):

                r = RedesOut(
                    rede = m.redes[j].rede, #mudar para string se necessário
                    ideb2017 = m.redes[j].ideb2017,
                    ideb2019 = m.redes[j].ideb2019,
                    ideb2021 = m.redes[j].ideb2021,
                    ideb2023 = m.redes[j].ideb2023
                )

                list_redes.append(r)

            munout = MunicipioOut(
                cod_municipio = m.cod_municipio,
                nome = m.nome,
                estado = state_value,
                redes = list_redes
            )

            lista_municipios.municipios.append(munout)
    
    return lista_municipios

def extract_town_by_name(r:Trie_Root, name : str) -> ListMunicipioOut:
    offsets = []
    aux  = []
    lista_municipios = ListMunicipioOut(municipios = [])

    aux = r.states[0].search(name)
    offsets.extend(aux)
    aux = r.states[1].search(name)
    offsets.extend(aux)
    aux = r.states[2].search(name)
    offsets.extend(aux)

    if len(offsets) == 0:
        return ListMunicipioOut(municipios = [])

    path = os.path.join(os.path.dirname(__file__), "data.bin")

    with open(path, "rb") as f:
        for i in offsets:
            f.seek(i)
            buf = f.read(TOTAL_SIZE)
            if not buf:
                break
            m = Municipio.get_bytes(buf)

            if m.estado == 0:
                state_value = 'RS'
            elif m.estado == 1:
                state_value = 'SC'
            else:
                state_value = 'PR'

            list_redes: list[RedesOut] = []


            for j in range(NUM_REDES):

                r = RedesOut(
                    rede = m.redes[j].rede, #mudar para string se necessário
                    ideb2017 = m.redes[j].ideb2017,
                    ideb2019 = m.redes[j].ideb2019,
                    ideb2021 = m.redes[j].ideb2021,
                    ideb2023 = m.redes[j].ideb2023
                )

                list_redes.append(r)

            munout = MunicipioOut(
                cod_municipio = m.cod_municipio,
                nome = m.nome,
                estado = state_value,
                redes = list_redes
            )

            lista_municipios.municipios.append(munout)
        
    return lista_municipios

def extract_state_name(r:Trie_Root, name : str, state:int) -> ListMunicipioOut:
    
    lista_municipios = ListMunicipioOut(municipios = [])
    offsets = r.states[state].search(name)

    if len(offsets) == 0:
        return lista_municipios

    offset = offsets[0]

    path = os.path.join(os.path.dirname(__file__), "data.bin")

    with open(path, "rb") as f:
        f.seek(offset)
        buf = f.read(TOTAL_SIZE)

        m = Municipio.get_bytes(buf)

        if m.estado == 0:
            state_value = 'RS'
        elif m.estado == 1:
            state_value = 'SC'
        else:
            state_value = 'PR'

        list_redes: list[RedesOut] = []


        for j in range(NUM_REDES):

            r = RedesOut(
                rede = m.redes[j].rede, #mudar para string se necessário
                ideb2017 = m.redes[j].ideb2017,
                ideb2019 = m.redes[j].ideb2019,
                ideb2021 = m.redes[j].ideb2021,
                ideb2023 = m.redes[j].ideb2023
            )

            list_redes.append(r)

        munout = MunicipioOut(
            cod_municipio = m.cod_municipio,
            nome = m.nome,
            estado = state_value,
            redes = list_redes
        )

        lista_municipios.municipios.append(munout)
    
    return lista_municipios





    
    

