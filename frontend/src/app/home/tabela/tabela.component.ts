import { Component, OnInit } from '@angular/core';
import { DataService } from '../../data.service';

interface Dados {
  estado: string, 
  cidade: string, 
  tipo: string, 
  ideb2019: number, 
  ideb2021: number, 
  ideb2023: number
}

@Component({
  selector: 'app-tabela',
  imports: [],
  templateUrl: './tabela.component.html',
  styleUrl: './tabela.component.css'
})
export class TabelaComponent implements OnInit{
  constructor(private DataService: DataService){}
  data: Dados[] = []

  ngOnInit(){
    this.data = this.DataService.getData()
  }
}
