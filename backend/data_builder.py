import pandas as pd
from pandas import DataFrame
import os
from BTrees.OOBTree import OOBTree
import pickle
from trees import *
from file_and_types import *

# ++++++++++++++++++++++++++++++++++
# + FAVOR explicar utilidade disso!
# ++++++++++++++++++++++++++++++++++

CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzáàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ -'
CHAR_TO_INDEX = {c: i for i, c in enumerate(CHARSET)}
INDEX_TO_CHAR = {i: c for i, c in enumerate(CHARSET)}
MAX_CHILDREN = len(CHARSET)
MAX_OFFSETS = 3  # número fixo de offsets
NODE_SIZE = 1 + 4 * MAX_OFFSETS + 4 * MAX_CHILDREN  # total em bytes por nó
    

class DataFactory:
    data = pd.DataFrame()
    
    def load_csv(self, csv_path: str) -> None:
        """Loads a dataframe based on a csv"""
        self.data = pd.read_csv(csv_path)
    
    def filter_by_states (self, states: list) -> None:
        """Given a list of states, filters the dataframe"""
        self.data = self.data[self.data['SG_UF'].isin(states)]
            
    def _state_value (self, state: str) -> int:
        if state == "RS":
            return 0
        if state == "SC":
            return 1
        
        return 2

    def _rede_value (self, rede: str) -> int:
        if rede == "Pública":
            return REDE_PUBLICA
        if rede == "Estadual":
            return REDE_ESTADUAL
        
        return REDE_FEDERAL

    def ideb_value (self, value_str: str) -> float:
        if value_str != '-':
            return float(value_str)
        return 0
        
    def pipeline_to_file(self, path_to_file: str):
        """
        Loads csv data into a dataframe, applies the necessary filters and aggregates the data.
        Writes the result to a binary file
        """
        
        self.load_csv(path_to_file)
        self.filter_by_states(['RS', 'SC', 'PR'])
        
        
        grouped_data = self.data.groupby(['COD_MUNICIPIO'])
        
        with open('data.bin', 'wb') as f, open('saeb.bin', 'wb') as f2:
            
            counter = 0
            prefix_root_tree = Trie_Root()
            btree = OOBTree() #Criamos uma Btree
            

            for _, group_df in grouped_data:
                # Gather info from each town
                sg_uf = group_df['SG_UF'].iloc[0]
                cod_municipio = group_df['COD_MUNICIPIO'].iloc[0]
                nome_municipio = group_df['NOME_MUNICIPIO'].iloc[0]

                saebData = MunicipioSaeb(cod_municipio)

                redes_data: list[Rede] = []
                
                # map which rede exists
                existing_rede = {REDE_PUBLICA: None, REDE_ESTADUAL: None, REDE_FEDERAL: None}
                
                for _, row in group_df.iterrows():
                    offset_data_bin = f.tell()
                    offset_saeb_bin = f2.tell()
                    
                    rede_type = self._rede_value(row['REDE'])
                    
                    rede = Rede(
                        rede=rede_type,
                        ideb2017=self.ideb_value(row['IDEB_2017']),
                        ideb2019=self.ideb_value(row['IDEB_2019']),
                        ideb2021=self.ideb_value(row['IDEB_2021']),
                        ideb2023=self.ideb_value(row['IDEB_2023'])
                    )
                    
                    existing_rede[rede_type] = rede
                    
                    saebData.add_rede(rede_type);
                    
                    rede_saeb_atual = saebData.get_rede(rede_type)
                    
                    rede_saeb_atual.set_saeb(2017, math = safe_float(row['SAEB_MAT_2017']), port = safe_float(row['SAEB_PORT_2017']), final = safe_float(row['SAEB_NOTA_2017']))
                    rede_saeb_atual.set_saeb(2019, math = safe_float(row['SAEB_MAT_2019']), port = safe_float(row['SAEB_PORT_2019']), final = safe_float(row['SAEB_NOTA_2019']))
                    rede_saeb_atual.set_saeb(2021, math = safe_float(row['SAEB_MAT_2021']), port = safe_float(row['SAEB_PORT_2021']), final = safe_float(row['SAEB_NOTA_2021']))
                    rede_saeb_atual.set_saeb(2023, math = safe_float(row['SAEB_MAT_2023']), port = safe_float(row['SAEB_PORT_2023']), final = safe_float(row['SAEB_NOTA_2023']))
                    
                    pickle.dump(saebData, f2)

                    for i in range(NUM_REDES):
                        if existing_rede[i]:
                            redes_data.append(existing_rede[i])
                        else:
                            redes_data.append(Rede.empty())
                            
                m = Municipio(
                    cod_municipio=cod_municipio,
                    nome=nome_municipio,
                    estado=self._state_value(sg_uf),
                    redes=redes_data 
                )
                
                f.write(m.to_bytes())
                
                # Building indices                
                prefix_root_tree.states[self._state_value(sg_uf)].insert(nome_municipio, offset_data_bin)
                
                mun_btree = MunicipioBTreeEntry(cod_municipio, offset_data_bin, offset_saeb_bin);
                btree[cod_municipio] = mun_btree

            return prefix_root_tree, btree
        

def initialize_api():

    nome_trie = "trie.bin"
    nome_data = "data.bin"
    nome_b = "btree.bin"
    nome_saeb = "saeb.bin"

    r = Trie_Root()
    b = OOBTree()

    datafact = DataFactory()


    if os.path.exists(nome_data):
        if os.path.exists(nome_saeb):
            if os.path.exists(nome_trie):
                if os.path.exists(nome_b):
                    r = TreeHandler.load_trie_root()
                    b = TreeHandler.load_btree()
                else:
                    r, b = datafact.pipeline_to_file("data.csv")
                    TreeHandler.save_btree(b)
                    TreeHandler.save_trie_root(r)
            else:
                r, b = datafact.pipeline_to_file("data.csv")
                TreeHandler.save_btree(b)
                TreeHandler.save_trie_root(r)
        else:
            r, b = datafact.pipeline_to_file("data.csv")
            TreeHandler.save_btree(b)
            TreeHandler.save_trie_root(r)
    else:
        r, b = datafact.pipeline_to_file("data.csv")
        TreeHandler.save_btree(b)
        TreeHandler.save_trie_root(r)
    
    return r,b

                    
        

def safe_float(value) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0