import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DataService } from '../../data.service';
import { ApiService } from '../../api.service';
import {ApiResponse, Municipio, UnwoundMunicipio} from '../../models/cities'
import { filtros } from '../../models/filtos';
import { FiltroService } from '../../filtro-service.service';
import { debounceTime, distinctUntilChanged, switchMap, Observable, of, tap } from 'rxjs';
import {map} from 'rxjs/operators';

@Component({
  selector: 'app-tabela',
  imports: [CommonModule],
  templateUrl: './tabela.component.html',
  styleUrl: './tabela.component.css'
})
export class TabelaComponent implements OnInit{
  private data_manager = inject(DataService)
  private filter_service = inject(FiltroService)

  public data: Observable<UnwoundMunicipio[]> = of([]);

  ngOnInit(){
    this.data = this.filter_service.filtrosAtuais$.pipe(
      debounceTime(300),
      distinctUntilChanged((prev, curr) => prev == curr),
      switchMap((filtros: filtros) => this.data_manager.getDados(filtros)),
      tap(municipios => this.data_manager.updateCurrData(municipios)),
      map(municipios => this.data_manager.unwind(municipios))
    )
  }

  truncateFloat(num: number){
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
}
