import { Component } from '@angular/core';
import { TabelaComponent } from './tabela/tabela.component';
import { NavbarComponent } from './navbar/navbar.component';
import { SearchComponent } from './search/search.component';
import { InfoComponent } from "./info/info.component";

@Component({
  selector: 'app-home',
  imports: [TabelaComponent, NavbarComponent, SearchComponent, InfoComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

}
