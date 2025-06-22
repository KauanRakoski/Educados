import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';
import { RouterModule } from '@angular/router';
import { DataService } from './data.service';
import {ApiService} from '../app/api.service'


@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';  
  private data_manager = inject(DataService);
  private api = inject(ApiService);


}
