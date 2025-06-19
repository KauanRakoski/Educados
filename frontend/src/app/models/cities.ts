
export interface Rede {
    rede: number,
    ideb2017: number,
    ideb2019: number,
    ideb2021: number
    ideb2023: number
}

export interface Municipio {
    cod_municipio: number
    nome: string,
    estado: string,
    redes: Rede[]
}

export interface ApiResponse {
    municipios: Municipio[]
}

export type UnwoundMunicipio = Omit<Municipio, 'redes'> & Rede