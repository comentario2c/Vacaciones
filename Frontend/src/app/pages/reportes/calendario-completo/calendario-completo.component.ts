import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

interface VacacionesPorTrabajador {
  rut: string;
  nombre: string;
  cargo: string;
  dias: string[]; // fechas en formato 'YYYY-MM-DD'
}

interface SaldoCompleto {
  rut: string;
  anio: number;
  vacaciones_base: number;
  dias_progresivos: number;
  dias_pendientes: number;
  dias_tomados: number;
  total_disponible: number;
  total_a_planificar: number;
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

  progresivosPorRut: Record<string, number | undefined> = {};
  pendientesPorRut: Record<string, number | undefined> = {};
  totalPorRut: Record<string, number | undefined> = {};
  pedidosPorRut: Record<string, number | undefined> = {};
  saldoPorRut: Record<string, number | undefined> = {};

  numerosVacacionesPorTrabajador: Record<string, Record<string, number>> = {};

  feriados: Set<string> = new Set();

  cargoColores = new Map<string, string>([
    // Grupo 1 – Verde menta
    ['Bodega Grupo 1', 'bg-emerald-200'],
    ['Operador maquina de herramienta Grupo 1', 'bg-emerald-200'],
    ['Mecánico de banco Grupo 1', 'bg-emerald-200'],
    ['Soladores Grupo 1', 'bg-emerald-200'],
    ['Operador mesa de corte grupo 1', 'bg-emerald-200'],
    ['Secretaria Grupo 1', 'bg-emerald-200'],
  
    // Grupo 2 – Azul cielo
    ['Bodega Grupo 2', 'bg-sky-200'],
    ['Operador maquina de herramienta Grupo 2', 'bg-sky-200'],
    ['Mecánico de banco Grupo 2', 'bg-sky-200'],
    ['Soladores Grupo 2', 'bg-sky-200'],
    ['Secretaria Grupo 2', 'bg-sky-200'],
  
    // Grupo 3 – Gris cálido
    ['Bodega Grupo 3', 'bg-zinc-200'],
    ['Soladores Grupo 3', 'bg-zinc-200'],
  
    // Administrativos – Celeste claro
    ['Administrativos', 'bg-cyan-200'],
  ]);

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.cargarFeriados().then(() => this.cargarDatos());
 
  }

  async cargarFeriados(): Promise<void> {
    try {
      const data = await this.http.get<string[]>('http://localhost:8000/api/vacaciones/feriados').toPromise();
      this.feriados = new Set(data);
    } catch (err) {
      console.error('Error al cargar feriados:', err);
    }
  }

  esLaboral(fecha: Date): boolean {
    const dia = fecha.getDay(); // 0 = domingo, 6 = sábado
    const fechaStr = this.formatoFecha(fecha);
    return dia !== 0 && dia !== 6 && !this.feriados.has(fechaStr);
  }

  cargarDatos(): void {
    this.http.get<VacacionesPorTrabajador[]>(`http://localhost:8000/api/vacaciones/reporte?anio=${this.anioSeleccionado}`)
      .subscribe({
        next: (data) => {
          this.trabajadores = data;
          this.sinDatos = data.length === 0;
          this.generarDiasCalendario();
          this.generarNumeracionVacaciones();
  
          if (!this.sinDatos) {
            this.trabajadores.sort((a, b) => {
              const familiaA = this.getFamiliaCargo(a.cargo);
              const familiaB = this.getFamiliaCargo(b.cargo);
              return familiaA.localeCompare(familiaB);
            });
            this.cargarSaldosCompletos();
          }
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
        const fecha = new Date(anio, mes, d);
        fechas.push(fecha);
      }
    });

    this.diasCalendario = fechas.sort((a, b) => a.getTime() - b.getTime());
    
  }

  cambiarAnio(event: any): void {
    this.anioSeleccionado = parseInt(event.target.value, 10);
    this.cargarDatos();
  }

  tieneVacacionesEn(fecha: Date, trabajador: VacacionesPorTrabajador): boolean {
    const fechaStr = this.formatoFecha(fecha);
    return trabajador.dias.includes(fechaStr) && this.esLaboral(fecha);
  }

  formatoFecha(fecha: Date): string {
    const año = fecha.getFullYear();
    const mes = String(fecha.getMonth() + 1).padStart(2, '0');
    const dia = String(fecha.getDate()).padStart(2, '0');
    return `${año}-${mes}-${dia}`;
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

  generarNumeracionVacaciones(): void {
    this.numerosVacacionesPorTrabajador = {};
  
    for (const trabajador of this.trabajadores) {
      const diasNumerados: Record<string, number> = {};
      let contador = 1;
  
      const diasOrdenados = [...trabajador.dias].sort((a, b) => a.localeCompare(b));
  
      for (const fechaStr of diasOrdenados) {
        const fecha = new Date(fechaStr + 'T00:00:00');
        const fechaFormateada = this.formatoFecha(fecha);
        const esDiaLaboral = this.esLaboral(fecha);
  
        if (esDiaLaboral) {
          diasNumerados[fechaFormateada] = contador++;
        }
      }
      this.numerosVacacionesPorTrabajador[trabajador.rut] = diasNumerados;
    }
  }

  exportarCalendarioPDF(): void {
    const elemento = document.getElementById('contenedor-calendario');
    if (!elemento) return;
  
    // 🟢 Asegura que el ancho real esté aplicado antes de capturar
    const anchoOriginal = elemento.style.width;
    elemento.style.width = elemento.scrollWidth + 'px';
  
    html2canvas(elemento, {
      scale: 3,
      useCORS: true,
      backgroundColor: '#ffffff'
    }).then(canvas => {
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('l', 'mm', [300, 841]);
      const imgProps = pdf.getImageProperties(imgData);
      const margin = 10; // 10mm = 1cm
      const usableWidth = pdf.internal.pageSize.getWidth() - margin * 2;
      const usableHeight = (imgProps.height * usableWidth) / imgProps.width;
  
      pdf.addImage(imgData, 'PNG', margin, margin, usableWidth, usableHeight);
      pdf.save(`reporte-vacaciones-${this.anioSeleccionado}.pdf`);
  
      // 🔙 Restaurar el ancho original
      elemento.style.width = anchoOriginal;
    });
  }

  cargarSaldosCompletos(): void {
    this.http.get<SaldoCompleto[]>(`http://localhost:8000/api/calculos/saldos-completos/${this.anioSeleccionado}`)
      .subscribe({
        next: (data) => {
          for (const saldo of data) {
            const rut = saldo.rut;
            this.progresivosPorRut[rut] = saldo.dias_progresivos;
            this.pendientesPorRut[rut] = saldo.dias_pendientes;
            this.totalPorRut[rut] = saldo.total_disponible;
            this.pedidosPorRut[rut] = saldo.dias_tomados;
            this.saldoPorRut[rut] = saldo.total_a_planificar;
          }
        },
        error: (err) => {
          console.error('Error al cargar saldos completos:', err);
        }
      });
  }

  getFamiliaCargo(cargo: string): string {
    return cargo.split(' Grupo')[0].trim().toLowerCase(); // Normaliza el nombre base
  }
}