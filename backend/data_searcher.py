from file_and_types import *
import os
import struct
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
from BTrees.OOBTree import OOBTree


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

    aux = r.states[0].starts_with_offset(name)
    offsets.extend(aux)
    aux = r.states[1].starts_with_offset(name)
    offsets.extend(aux)
    aux = r.states[2].starts_with_offset(name)
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
    offsets = r.states[state].starts_with_offset(name)

    if len(offsets) == 0:
        return lista_municipios


    path = os.path.join(os.path.dirname(__file__), "data.bin")

    with open(path, "rb") as f:

        for i in offsets:
            f.seek(i)
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



def extract_town_at_offset(offset: int, 
                           path: str = None, 
                           total_size: int = TOTAL_SIZE
                          ) -> MunicipioOut | None:
    """
    Lê exatamente um município a partir de `offset` no arquivo `data.bin`
    e retorna o objeto MunicipioOut correspondente, ou None se não houver
    bytes suficientes.
    """
    # usa o mesmo data.bin do módulo (ou receba path customizado)
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "data.bin")

    with open(path, "rb") as f:
        f.seek(offset)
        buf = f.read(total_size)
        if len(buf) < total_size:
            # não há dado completo ali
            return None

        # desserializa para a estrutura interna
        m = Municipio.get_bytes(buf)

    # converte o código de estado em string
    if   m.estado == 0: state_value = 'RS'
    elif m.estado == 1: state_value = 'SC'
    else:               state_value = 'PR'

    # mapea as redes internas para o output
    list_redes: list[RedesOut] = []
    for rede_entry in m.redes[:NUM_REDES]:
        r_out = RedesOut(
            rede     = rede_entry.rede,
            ideb2017 = rede_entry.ideb2017,
            ideb2019 = rede_entry.ideb2019,
            ideb2021 = rede_entry.ideb2021,
            ideb2023 = rede_entry.ideb2023
        )
        list_redes.append(r_out)

    # monta e retorna o MunicipioOut
    return MunicipioOut(
        cod_municipio = m.cod_municipio,
        nome          = m.nome,
        estado        = state_value,
        redes         = list_redes
    )

def extract_saeb(cod_mun: int, b: OOBTree):
    main_offset = b[cod_mun].main_data_offset;
    print(extract_town_at_offset(main_offset))





    
    

