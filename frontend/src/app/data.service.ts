// src/app/services/data.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { map, catchError, tap } from 'rxjs/operators';
import { ApiResponse, Municipio, UnwoundMunicipio } from './models/cities';
import { filtros } from './models/filtos';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private readonly API_BASE_URL = 'http://localhost:5000';

  private dadosAtuaisSubject = new BehaviorSubject<Municipio[]>([]);
  public dadosAtuais$ = this.dadosAtuaisSubject.asObservable();

  constructor (private http: HttpClient){}


  getAll(): Observable<Municipio[]>{
    return this.http.get<ApiResponse>(`${this.API_BASE_URL}/dados`).pipe(
      map((response: ApiResponse) => response.municipios)
    )
  }

  getDados(filtros: filtros): Observable<Municipio[]>{
    return this.http.get<ApiResponse>(`${this.API_BASE_URL}/dados?state=${filtros.estado}&name=${filtros.name}`).pipe(
      map((response: ApiResponse) => response.municipios)
    )
  }

  unwind(data: Municipio[]): UnwoundMunicipio[] {
    if (!data) return [];
    return data.flatMap(municipio => {
      const { redes, ...otherInfo } = municipio;
      const redesValidas = redes.filter(rede => rede.rede !== -1);
      return redesValidas.map(rede => ({
        ...otherInfo,
        ...rede
      }));
    });
  }

  updateCurrData (dados: Municipio[]){
    this.dadosAtuaisSubject.next(dados)
  }
}
