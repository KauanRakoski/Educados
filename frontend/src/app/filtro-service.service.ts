import { Injectable } from '@angular/core';
import { filtros } from './models/filtos';
import { BehaviorSubject, combineLatest, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class FiltroService {

  private nameSubject = new BehaviorSubject<string>('')
  private estadoSubject = new BehaviorSubject<string>('')
  private redeSubject = new BehaviorSubject<number>(3)
  
 
  // Observável público que agrega os filtros
  public filtrosAtuais$ = new Observable<filtros>

  constructor() {
    this.filtrosAtuais$ = combineLatest([this.nameSubject, this.estadoSubject, this.redeSubject]).pipe(
      map(([name, estado, rede]) => ({
        name,
        estado,
        rede
      }))
    )
  }

  public updateNameFilter (name: string): void{
    this.nameSubject.next(name);
  }

  public updateEstadoFilter (estado: string): void{
    this.estadoSubject.next(estado);
  }

  public updateRedeFilter(rede: number): void {
    this.redeSubject.next(rede);
  }
}
