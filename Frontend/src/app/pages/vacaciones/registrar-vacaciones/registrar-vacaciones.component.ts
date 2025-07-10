import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Vacaciones } from '../../../shared/models/vacaciones.models';
import { CalendarioComponent } from '../calendario/calendario.component';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-registrar-vacaciones',
  standalone: true,
  imports: [CommonModule, FormsModule, CalendarioComponent],
  templateUrl: './registrar-vacaciones.component.html',
  styleUrl: './registrar-vacaciones.component.css'
})
export class RegistrarVacacionesComponent {
  // Objetos y variables
  vacaciones: Vacaciones = {
    RutTrabajador: '',
    FechaInicio: '',
    FechaFin: '',
    DiasTomados: 0,
    Observaciones: ''
  };

  diasMesActual: number[] = [];
  diasMesSiguiente: number[] = [];
  ultimaFechaTomada: string = '';

  meses: { mes: number; anio: number; dias: number[] }[] = [];

  trabajadores: { Nombre: string; RutTrabajador: string }[] = [];
  busqueda: string = '';
  trabajadorSeleccionado: string = '';

  constructor(private router: Router, private http: HttpClient) {}

  // ------------------------------ Barra de busqueda ------------------------------
  cargarTrabajadores() {
    this.http.get<{ Nombre: string; RutTrabajador: string }[]>('http://localhost:8000/api/trabajadores')
      .subscribe(trabajadores => {
        this.trabajadores = trabajadores;
      });
  }

  ngOnInit() {
    this.cargarTrabajadores();
  }

  seleccionarTrabajador(nombre: string) {
    const trabajador = this.trabajadores.find(t => t.Nombre === nombre);
    if (trabajador) {
      this.vacaciones.RutTrabajador = trabajador.RutTrabajador;
      this.trabajadorSeleccionado = trabajador.Nombre;
      this.busqueda = trabajador.Nombre;
    }
  }

  get trabajadoresFiltrados() {
    const termino = this.busqueda?.toLowerCase() ?? '';
    return this.trabajadores.filter(t =>
      t.Nombre.toLowerCase().includes(termino)
    );
  }

  esNombreExacto(nombre: string): boolean {
    return this.trabajadores.some(t => t.Nombre.toLowerCase() === nombre.toLowerCase());
  }

  // ------------------------------ Calendario dinamico ------------------------------
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
        this.ultimaFechaTomada = aFechaISO(fecha);
        restantes--;
      }
      fecha.setDate(fecha.getDate() + 1);
    }
    this.vacaciones.FechaFin = this.ultimaFechaTomada;
  }

  // ------------------------------ Validaciones ------------------------------
  validarDiasTomados() {
    const maximo = 50;
    if (this.vacaciones.DiasTomados > maximo) {
      this.vacaciones.DiasTomados = maximo;
    }
    this.actualizarCalendario();
  }

  // ------------------------------ Funciones ------------------------------
  obtenerNombreMes(mes: number): string {
    return new Date(2000, mes).toLocaleString('es-CL', { month: 'long' }).replace(/^\w/, c => c.toUpperCase());
  }

  // ------------------------------ Conectar con el backend ------------------------------

  registrarVacaciones() {
    this.http.post('http://localhost:8000/api/vacaciones/crear', this.vacaciones).subscribe({
      next: res => {
        console.log('Vacaciones registradas:', res);
        this.router.navigate(['/menu']);
      },
      error: err => {
        console.error('Error al registrar vacaciones:', err.error);
      }
    });
  }
}