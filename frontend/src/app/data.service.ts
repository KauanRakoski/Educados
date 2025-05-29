import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor() { }

  private data = [
    {estado: 'RS', cidade: 'Ijuí', tipo: 'pública', ideb2019: 4.5, ideb2021: 4.8, ideb2023: 4.9},
  ]

  getData(){
    return this.data;
  }

  setData(data: {estado: string, cidade: string, tipo: string, ideb2019: number, ideb2021: number, ideb2023: number}[]){
    this.data = data;
  }
}
