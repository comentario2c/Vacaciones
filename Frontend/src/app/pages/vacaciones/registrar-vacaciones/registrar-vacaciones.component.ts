import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Vacaciones } from '../../../shared/models/vacaciones.models';
import { CalendarioComponent } from '../calendario/calendario.component';

@Component({
  selector: 'app-registrar-vacaciones',
  standalone: true,
  imports: [CommonModule, FormsModule, CalendarioComponent],
  templateUrl: './registrar-vacaciones.component.html',
  styleUrl: './registrar-vacaciones.component.css'
})
export class RegistrarVacacionesComponent {
  
  // Formulario y calendario dinamico 
  vacaciones: Vacaciones = {
    RutTrabajador: '',
    FechaInicio: '',
    FechaFin: '',
    DiasTomados: 0,
    Observaciones: ''
  };

  diasMesActual: number[] = [];
  diasMesSiguiente: number[] = [];

  meses: { mes: number; anio: number; dias: number[] }[] = [];

  constructor(private router: Router) {}

  actualizarCalendario() {
    if (!this.vacaciones.FechaInicio || !this.vacaciones.DiasTomados) return;

    const feriados = ['']; // puedes agregar más feriados

    this.meses = [];
    this.diasMesActual = [];
    this.diasMesSiguiente = [];
  
    let restantes = this.vacaciones.DiasTomados;
    const [año, mes, dia] = this.vacaciones.FechaInicio.split('-').map(Number);
    let fecha = new Date(año, mes - 1, dia);
  
    function aFechaISO(fecha: Date): string {
      const yyyy = fecha.getFullYear();
      const mm = String(fecha.getMonth() + 1).padStart(2, '0'); // +1 porque enero es 0
      const dd = String(fecha.getDate()).padStart(2, '0');
      return `${yyyy}-${mm}-${dd}`;
    }

    // 🔁 Recorre los días hasta completar los días tomados
    while (restantes > 0) {
      const iso = aFechaISO(fecha);
      const diaSemana = fecha.getDay();
      const esLaboral = diaSemana !== 0 && diaSemana !== 6 && !feriados.includes(iso);

      const yyyy = fecha.getFullYear();
      const mm = fecha.getMonth();
      const dd = fecha.getDate();
  
      if (esLaboral) {
        // Busca si ya hay un mes-anio agregado
        let mesExistente = this.meses.find(m => m.mes === mm && m.anio === yyyy);
        if (!mesExistente) {
          mesExistente = { mes: mm, anio: yyyy, dias: [] };
          this.meses.push(mesExistente);
        }
        mesExistente.dias.push(dd);
        restantes--;
      }
      fecha.setDate(fecha.getDate() + 1);
    }
  }

  validarDiasTomados() {
    const maximo = 50;
    if (this.vacaciones.DiasTomados > maximo) {
      this.vacaciones.DiasTomados = maximo;
    }
    this.actualizarCalendario();
  }
  
  obtenerNombreMes(mes: number): string {
    return new Date(2000, mes).toLocaleString('es-CL', { month: 'long' }).replace(/^\w/, c => c.toUpperCase());
  }

  // Conectar con el backend


}