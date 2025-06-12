import { Component, OnInit, inject } from '@angular/core';
import { DataService } from '../../data.service';
import { ApiService } from '../../api.service';
import {ApiResponse, Municipio} from '../../models/cities'

@Component({
  selector: 'app-tabela',
  imports: [],
  templateUrl: './tabela.component.html',
  styleUrl: './tabela.component.css'
})
export class TabelaComponent implements OnInit{
  private api = inject(ApiService)

  data: Municipio[] = []

  async ngOnInit(){
    let response: ApiResponse = await this.api.get<ApiResponse>("/dados");
    this.data = response.municipios;
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
