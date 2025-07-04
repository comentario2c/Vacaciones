import { CommonModule } from '@angular/common';
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-calendario',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './calendario.component.html',
  styleUrl: './calendario.component.css'
})
export class CalendarioComponent implements OnChanges {
  @Input() mes: number = 0;          // enero = 0
  @Input() anio: number = 2025;
  @Input() diasMarcados: number[] = [];
  @Input() titulo: string = 'Calendario';

  diasDelMes: {
    dia: number | null;
    fecha?: string;
    esLaboral?: boolean;
    tomado?: boolean;
  }[] = [];

  ngOnChanges(_: SimpleChanges) {
    this.generarCalendario();
  }

  private generarCalendario() {
    this.diasDelMes = [];
    
    const feriados = ['']; // Usar este array para los feriados

    const primerDiaMes = new Date(this.anio, this.mes, 1);
    const diasEnMes = new Date(this.anio, this.mes + 1, 0).getDate();

    let offset = (primerDiaMes.getDay() + 6) % 7;
    while (offset--) this.diasDelMes.push({ dia: null });

    for (let i = 1; i <= diasEnMes; i++) {
      const actual = new Date(this.anio, this.mes, i);
      const diaSemana = actual.getDay();
      const fechaISO = actual.toISOString().split('T')[0];
      const esFeriado = feriados.includes(fechaISO);
      const esLaboral = diaSemana !== 0 && diaSemana !== 6 && !esFeriado;
      const tomado = this.diasMarcados.includes(i);

      this.diasDelMes.push({
        dia: i,
        fecha: fechaISO,
        esLaboral,
        tomado
      });
    }
  }

  get nombreMes(): string {
    return new Date(this.anio, this.mes)
      .toLocaleString('es-CL', { month: 'long' })
      .replace(/^\w/, c => c.toUpperCase());
  }
}