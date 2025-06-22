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
          data: [0, 0, 0],
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

        this.updateGraph(municipiosUnwound)
      })
    }
    
    updateGraph(data: UnwoundMunicipio[]){
      let meanByState = this.calcMeanByState(data)
      let meanByYear = this.calcMeanByYear(data);
      let states: string[] = ["RS", "SC", "PR"];

      let removed = 0;

      meanByState.forEach((mean, index) => {
        if (mean == 0){
          states.splice(index - removed, 1);
          removed++;
        }
      })

      this.chartOptions.series = [{
        data: meanByYear
      }]

      this.BarChartOpt.series = [{
        data: meanByState.filter(n => n != 0)
      }]

      this.BarChartOpt.xaxis = {
        categories: states
      }
    }

    calcMeanByState(data: UnwoundMunicipio[]){
      // RS, SC, PR
      let sumByState = [0, 0, 0];

      sumByState[0] = this.calcMeanByYear(data.filter(m => m.estado == 'RS')).reduce((prev, curr) => {
        return prev + curr;
      }, 0);

      sumByState[1] = this.calcMeanByYear(data.filter(m => m.estado == 'SC')).reduce((prev, curr) => {
        return prev + curr;
      }, 0);

      sumByState[2] = this.calcMeanByYear(data.filter(m => m.estado == 'PR')).reduce((prev, curr) => {
        return prev + curr;
      }, 0);

      return sumByState.map(sum => Number.parseFloat((sum / 4).toFixed(2)));
    }

    calcMeanByYear(data: UnwoundMunicipio[]){
      let means: number[] = [0, 0, 0, 0];
      let n: number[] = [0, 0, 0, 0];

      data.forEach(municipio => {
        if (municipio.ideb2017 > 0){
          means[0] += municipio.ideb2017;
          n[0]++;
        }
        if (municipio.ideb2019 > 0){
          means[1] += municipio.ideb2019;
          n[1]++;
        }
        if (municipio.ideb2021 > 0){
          means[2] += municipio.ideb2021;
          n[2]++;
        }
        if (municipio.ideb2023 > 0){
          means[3] += municipio.ideb2023;
          n[3]++;
        }
      })

      for (let i = 0; i < 4; i++){
        if (n[i] != 0)
          means[i] /= n[i];
        means[i] = Number.parseFloat(means[i].toFixed(2))
      }

      return means;
    }
  }
