import { Component, OnInit } from '@angular/core';
import {NgApexchartsModule} from 'ng-apexcharts'
import { DataService } from '../../data.service';

@Component({
  selector: 'app-info',
  imports: [NgApexchartsModule],
  templateUrl: './info.component.html',
  styleUrl: './info.component.css'
})
export class InfoComponent implements OnInit{
  constructor(private DataService: DataService){}
  years = []

  ngOnInit(): void {
      
  }
}
