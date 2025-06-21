import { Component, inject, OnInit, ViewChild } from '@angular/core';
import { DataService } from '../../data.service';
import { Observable } from 'rxjs';
import { UnwoundMunicipio } from '../../models/cities';

import {
  ChartComponent,
  ApexAxisChartSeries,
  ApexChart,
  ApexXAxis,
  ApexDataLabels,
  ApexTitleSubtitle,
  ApexStroke,
  ApexMarkers,
  ApexGrid
} from "ng-apexcharts";

export type ChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  xaxis: ApexXAxis;
  dataLabels: ApexDataLabels;
  grid: ApexGrid;
  markers: ApexMarkers;
  stroke: ApexStroke;
  title: ApexTitleSubtitle;
};

export type BarChartOpt = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  xaxis: ApexXAxis;
  dataLabels: ApexDataLabels;
  grid: ApexGrid;
  stroke: ApexStroke;
  title: ApexTitleSubtitle;
}

@Component({
  selector: 'app-info',
  imports: [ChartComponent],
  templateUrl: './info.component.html',
  styleUrl: './info.component.css'
})
export class InfoComponent implements OnInit{
  @ViewChild("chart") chart!: ChartComponent;
  public chartOptions: Partial<ChartOptions>;

  @ViewChild("estados") bar!: ChartComponent
  public BarChartOpt: Partial<BarChartOpt>;

  private data_manager = inject(DataService)
  years = []

  constructor(){
    this.chartOptions = {
      series: [
        {
          name: "Média por ano",
          data: [10, 41, 35, 51],
          color: "#4E71FC"
        }
      ],
      chart: {
        height: 250,
        width: 450,
        type: "line",
        zoom: {
          enabled: false
        }
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: "straight"
      },
      markers: {
        size: 6,
        hover: {
          size: 10
        }
      },
      title: {
        text: "Média IDEB por ano",
        align: "left"
      },
      grid: {
        row: {
          colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
          opacity: 0.5
        }
      },
      xaxis: {
        categories: [
          "2017",
          "2019",
          "2021",
          "2023"
        ]
      }
    } 

    this.BarChartOpt = {
      series: [
        {
          name: "Média por estado",
          data: [0, 0, 0, 0],
          color: "#4E71FC"
        }
      ],
      chart: {
        height: 250,
        width: 450,
        type: "bar",
        zoom: {
          enabled: false
        }
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: "straight"
      },
      title: {
        text: "Média IDEB por Estado",
        align: "left"
      },
      grid: {
        row: {
          colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
          opacity: 0.5
        }
      },
      xaxis: {
        categories: [
          "RS",
          "SC",
          "PR"
        ]
      }
    }}
  
    ngOnInit(){
      this.data_manager.dadosAtuais$.subscribe(municipios => {
        let municipiosUnwound: UnwoundMunicipio[] = this.data_manager.unwind(municipios);

        this.updateGraph()
      })
    }
    
    updateGraph(){
      this.chart.updateOptions([])
    }
  }
