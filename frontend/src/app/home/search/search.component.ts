import { Component, inject } from '@angular/core';
import { FiltroService } from '../../filtro-service.service';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-search',
  imports: [CommonModule],
  templateUrl: './search.component.html',
  styleUrl: './search.component.css'
})
export class SearchComponent {
  public filtroService = inject(FiltroService)

  updateNameFilter(event: Event): void {
    this.filtroService.updateNameFilter((event.target as HTMLInputElement).value);
  }

  onEstadoChange(event: Event): void {
    this.filtroService.updateEstadoFilter((event.target as HTMLSelectElement).value);
  }

  onRedeChange(event: Event): void {
    this.filtroService.updateRedeFilter(Number.parseInt((event.target as HTMLSelectElement).value));
  }
}
