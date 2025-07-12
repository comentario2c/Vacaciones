import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

interface VacacionesPorTrabajador {
  rut: string;
  nombre: string;
  cargo: string;
  dias: string[]; // fechas en formato 'YYYY-MM-DD'
}

@Component({
  selector: 'app-calendario-completo',
  templateUrl: './calendario-completo.component.html',
  styleUrls: ['./calendario-completo.component.css'],
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, HttpClientModule]
})
export class CalendarioCompletoComponent implements OnInit {

  anioSeleccionado: number = new Date().getFullYear();
  trabajadores: VacacionesPorTrabajador[] = [];
  diasCalendario: Date[] = []; // Fechas completas para mostrar en columnas
  sinDatos: boolean = false;

  cargoColores = new Map<string, string>([
    ['Administración', 'bg-blue-400'],
    ['Bodega', 'bg-green-400'],
    ['Mantenimiento', 'bg-yellow-400'],
    ['Soldador', 'bg-red-400'],
    ['Logística', 'bg-purple-400'],
  ]);

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.cargarDatos();
  }

  cargarDatos(): void {
    this.http.get<VacacionesPorTrabajador[]>(`http://localhost:8000/api/vacaciones/reporte?anio=${this.anioSeleccionado}`)
      .subscribe({
        next: (data) => {
          this.trabajadores = data;
          this.sinDatos = data.length === 0;
          this.generarDiasCalendario();
        },
        error: (err) => {
          console.error('Error al cargar el reporte:', err);
          this.trabajadores = [];
          this.diasCalendario = [];
          this.sinDatos = true;
        }
      });
  }

  getColorPorCargo(cargo: string): string {
    return this.cargoColores.get(cargo) || 'bg-gray-300';
  }

  generarDiasCalendario(): void {
    const mesesMostrados = new Set<string>();

    // Paso 1: determinar los meses involucrados
    this.trabajadores.forEach(trabajador => {
      trabajador.dias.forEach(fechaStr => {
        const fecha = new Date(fechaStr);
        const claveMes = `${fecha.getFullYear()}-${fecha.getMonth()}`;
        mesesMostrados.add(claveMes);
      });
    });

    // Paso 2: generar todos los días completos de esos meses
    const fechas: Date[] = [];

    mesesMostrados.forEach(clave => {
      const [anioStr, mesStr] = clave.split('-');
      const anio = parseInt(anioStr);
      const mes = parseInt(mesStr);
      const diasEnMes = new Date(anio, mes + 1, 0).getDate();

      for (let d = 1; d <= diasEnMes; d++) {
        fechas.push(new Date(anio, mes, d));
      }
    });

    this.diasCalendario = fechas.sort((a, b) => a.getTime() - b.getTime());
  }

  cambiarAnio(event: any): void {
    this.anioSeleccionado = parseInt(event.target.value, 10);
    this.cargarDatos();
  }

  tieneVacacionesEn(fecha: Date, trabajador: VacacionesPorTrabajador): boolean {
    return trabajador.dias.includes(this.formatoFecha(fecha));
  }

  formatoFecha(fecha: Date): string {
    return fecha.toISOString().split('T')[0];
  }

  nombreMes(fecha: Date): string {
    return fecha.toLocaleString('es-ES', { month: 'short' });
  }

  diaSemana(fecha: Date): string {
    return fecha.toLocaleString('es-ES', { weekday: 'short' });
  }

  diaMes(fecha: Date): number {
    return fecha.getDate();
  }
}