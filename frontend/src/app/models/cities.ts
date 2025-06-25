
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

export interface SaebGrades {
  math: number;
  port: number;
  final: number;
}

export interface MunicipioDetails {
  name: string;
  idebs: {
    rede: string;
    ideb2017: number;
    ideb2019: number;
    ideb2021: number;
    ideb2023: number;
  };
  saebs: {
    saeb2017: SaebGrades;
    saeb2019: SaebGrades;
    saeb2021: SaebGrades;
    saeb2023: SaebGrades;
  };
}

interface saebRedes {
    codigo_rede: number,
    saeb2017: SaebGrades;
    saeb2019: SaebGrades;
    saeb2021: SaebGrades;
    saeb2023: SaebGrades;
}

interface Saebs {
    cod_municipio: number,
    redes: saebRedes[]
}

export interface SaebResponse {
  municipio: {
    nome: string;
    redes: Rede[]; 
  };
  saeb: {
    redes: Saebs; 
  };
}

export type UnwoundMunicipio = Omit<Municipio, 'redes'> & Rede