import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DataService } from '../../data.service';
import { UnwoundMunicipio} from '../../models/cities'
import { filtros } from '../../models/filtos';
import { RouterLink } from '@angular/router';
import { FiltroService } from '../../filtro-service.service';
import { debounceTime, distinctUntilChanged, switchMap, Observable, of, tap, BehaviorSubject, combineLatest } from 'rxjs';
import {map, filter} from 'rxjs/operators';

@Component({
  selector: 'app-tabela',
  imports: [CommonModule, RouterLink],
  templateUrl: './tabela.component.html',
  styleUrl: './tabela.component.css'
})
export class TabelaComponent implements OnInit{
  private data_manager = inject(DataService)
  private filter_service = inject(FiltroService)

  public data: Observable<UnwoundMunicipio[]> = of([]);
  public sortOptions$ = new BehaviorSubject<{column: keyof UnwoundMunicipio | null, direction: 'asc' | 'desc'}>({
    column: null,
    direction: 'asc'
  })

  ngOnInit(){
    const unsortedData = this.filter_service.filtrosAtuais$.pipe(
      debounceTime(300),
      distinctUntilChanged((prev, curr) => prev == curr),
      switchMap((filtros: filtros) => {
        return this.data_manager.getDados(filtros).pipe(
          map(municipios => {
            if (filtros.rede > 2) return municipios;

            return municipios.map(municipio => {
              return {
                ...municipio,
                redes: municipio.redes.filter(rede => rede.rede == filtros.rede)
              }
            })
          })
        )
      }),
      tap(municipios => this.data_manager.updateCurrData(municipios)),
      map(municipios => this.data_manager.unwind(municipios)),
    )

    this.data = combineLatest([
      unsortedData,
      this.sortOptions$
    ]).pipe(map(([municipios, config]) => {
        if (!config.column) {
          return municipios;
        }

        return [...municipios].sort((a, b) => {
          const valorA = a[config.column!];
          const valorB = b[config.column!];

          let comparador = 0;
          if (valorA > valorB) {
            comparador = 1;
          } else if (valorA < valorB) {
            comparador = -1;
          }

          return config.direction === 'asc' ? comparador : -comparador;
        });
      })
    );
  }

  truncateFloat(num: number){
    if (num == 0)
      return '-'

    return num.toFixed(2)
  }

  redeFromCode(code: number){
    switch (code){
      case 0: 
        return "Pública"
      case 1:
        return "Estadual"
      case 2:
        return "Federal"
      default:
        return "Indefinido"
    }
  }

  orderBy(column: keyof UnwoundMunicipio){
    let currentConfig = this.sortOptions$.getValue()

    let newDirection: 'asc' | 'desc' = 'asc';

    if (currentConfig.column == column) {
      newDirection = currentConfig.direction == 'asc' ? 'desc' : 'asc';
    }

    console.log(currentConfig)
    this.sortOptions$.next({column: column, direction: newDirection})
    
  }
}
