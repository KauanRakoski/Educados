import { Component, OnInit, ViewChild } from '@angular/core';
import { NavbarComponent } from '../home/navbar/navbar.component';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { MunicipioDetails, SaebGrades, SaebResponse } from '../models/cities';
import { Observable, switchMap, map, tap } from 'rxjs';
import {
  ApexAxisChartSeries,
  ApexChart,
  ChartComponent,
  ApexDataLabels,
  ApexXAxis,
  ApexPlotOptions
} from "ng-apexcharts";

export type ChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  dataLabels: ApexDataLabels;
  plotOptions: ApexPlotOptions;
  xaxis: ApexXAxis;
};

@Component({
  selector: 'app-dashboard',
  imports: [NavbarComponent, CommonModule, ChartComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  @ViewChild("chart") chart!: ChartComponent;
  public chartOptions: Partial<ChartOptions>;
  details!: Observable<MunicipioDetails | null>;

  constructor(private route: ActivatedRoute, private http: HttpClient){
    this.chartOptions = {
      series: [
        {
          name: "Saeb Notas",
          data: [0, 0, 0, 0],
          color: "#4E71FC"
        }
      ],
      chart: {
        type: "bar",
        height: 300,
        width: 450
      },
      plotOptions: {
        bar: {
          horizontal: true
        }
      },
      dataLabels: {
        enabled: false
      },
      xaxis: {
        categories: [
          "Saeb 2017",
          "Saeb 2019",
          "Saeb 2021",
          "Saeb 2023"
        ]
      }
    };
  }

  ngOnInit(): void {
      this.details = this.route.params.pipe(
        switchMap(params => {
          let cod = params['cod'];
          let rede = params['rede'];

          return this.http.get<SaebResponse>(`http://localhost:5000/municipio/${cod}`).pipe(
            map(response => this.formatResponse(response, rede))
          )
        }),
        tap(details => {
          this.chartOptions.series = [{
            data: [details.saebs.saeb2017.final, 
              details.saebs.saeb2019.final, 
              details.saebs.saeb2021.final, 
              details.saebs.saeb2023.final]
          }]
        })
      )
  }

  formatResponse(response: any, rede: any): MunicipioDetails{
    
      const idebRede = response.municipio.redes.find((r: any) => r.rede == rede);
      const saebRede = response.saeb.redes.find((r: any) => r.codigo_rede == rede);
      console.log(saebRede)

      return {
      name: response.municipio.nome,
      idebs: idebRede,
      saebs: {
        saeb2017: saebRede.saeb2017,
        saeb2019: saebRede.saeb2019,
        saeb2021: saebRede.saeb2021,
        saeb2023: saebRede.saeb2023,
      }
    };
  }
}
