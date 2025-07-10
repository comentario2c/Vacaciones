import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-diasdisponibles',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './diasdisponibles.component.html',
  styleUrls: ['./diasdisponibles.component.css']
})
export class DiasdisponiblesComponent implements OnChanges {
  @Input() rutTrabajador: string = '';
  @Input() fecha: string = '';

  diasDisponibles: number | null = null;
  anioConsulta: number | null = null;

  constructor(private http: HttpClient) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (this.rutTrabajador && this.fecha) {
      const anio = Number(this.fecha.split('-')[0]);
      this.consultarDiasDisponibles(this.rutTrabajador, anio);
    } else {
      this.diasDisponibles = null;
      this.anioConsulta = null;
    }
  }

  private consultarDiasDisponibles(rut: string, anio: number) {
    this.http.get<{ DiasDisponibles: number }>(
      `http://127.0.0.1:8000/api/vacaciones/${rut}/dias-disponibles?anio=${anio}`
    ).subscribe({
      next: res => {
        this.diasDisponibles = res.DiasDisponibles;
        this.anioConsulta = anio;
      },
      error: err => {
        console.error('Error al obtener días disponibles:', err.error);
        this.diasDisponibles = null;
        this.anioConsulta = null;
      }
    });
  }
}