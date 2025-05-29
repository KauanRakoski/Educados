import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { RouterModule } from '@angular/router';
import { DataService } from './data.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'frontend';

  constructor(private DataService: DataService){}

  ngOnInit(){
    this.DataService.setData([
      {estado: 'RS', cidade: 'Ijuí', tipo: 'pública', ideb2019: 4.5, ideb2021: 4.8, ideb2023: 4.9},
      {estado: 'RS', cidade: 'Ijuí', tipo: 'privada', ideb2019: 4.5, ideb2021: 4.8, ideb2023: 4.9},
      {estado: 'RS', cidade: 'Porto Alegre', tipo: 'pública', ideb2019: 2.0, ideb2021: 0.4, ideb2023: 1.1}
    ])
  }
  
}
