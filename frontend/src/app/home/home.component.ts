import { Component } from '@angular/core';
import { TabelaComponent } from './tabela/tabela.component';

@Component({
  selector: 'app-home',
  imports: [TabelaComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

}
