import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Vacaciones } from '../../../shared/models/vacaciones.models';
import { CalendarioComponent } from '../calendario/calendario.component';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { DiasdisponiblesComponent } from '../diasdisponibles/diasdisponibles.component';

@Component({
  selector: 'app-formulario-vacaciones',
  standalone: true,
  imports: [CommonModule, FormsModule, CalendarioComponent, DiasdisponiblesComponent, HttpClientModule],
  templateUrl: './registrar-vacaciones.component.html',
  styleUrl: './registrar-vacaciones.component.css'
})
export class RegistrarVacacionesComponent {
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
  feriados: string[] = [];

  diasDisponibles: number | null = null;
  anioConsulta: number | null = null;

  trabajadores: { Nombre: string; RutTrabajador: string }[] = [];
  busqueda: string = '';
  trabajadorSeleccionado: string = '';

  advertenciaDiasSuperados: boolean = false;

  constructor(private router: Router, private http: HttpClient, private route: ActivatedRoute) {}

  ngOnInit() {
    // 1. Primero cargar feriados
    this.http.get<string[]>('http://localhost:8000/api/vacaciones/feriados')
      .subscribe(f => this.feriados = f);

    // 2. Luego cargar trabajadores y si hay ID, cargar vacaciones
    this.cargarTrabajadores().then(() => {
      const id = this.route.snapshot.paramMap.get('id');
      if (id) {
        this.http.get<Vacaciones>(`http://localhost:8000/api/vacaciones/${id}`).subscribe({
          next: data => {
            this.vacaciones = data;

            const trabajador = this.trabajadores.find(t => t.RutTrabajador === data.RutTrabajador);
            if (trabajador) {
              this.trabajadorSeleccionado = trabajador.Nombre;
              this.busqueda = trabajador.Nombre;
            }

            this.actualizarCalendario();
            this.actualizarDiasDisponibles();
          },
          error: err => console.error('Error al cargar vacaciones:', err.error)
        });
      }
    });
  }

  cargarTrabajadores(): Promise<void> {
    return new Promise(resolve => {
      this.http.get<{ Nombre: string; RutTrabajador: string }[]>('http://localhost:8000/api/trabajadores')
        .subscribe(trabajadores => {
          this.trabajadores = trabajadores;
          resolve();
        });
    });
  }

  seleccionarTrabajador(nombre: string) {
    const trabajador = this.trabajadores.find(t => t.Nombre === nombre);
    if (trabajador) {
      this.vacaciones.RutTrabajador = trabajador.RutTrabajador;
      this.trabajadorSeleccionado = trabajador.Nombre;
      this.busqueda = trabajador.Nombre;
      this.actualizarDiasDisponibles();
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

  actualizarCalendario() {
    if (!this.vacaciones.FechaInicio || !this.vacaciones.DiasTomados) return;

    this.meses = [];
    this.diasMesActual = [];
    this.diasMesSiguiente = [];

    let restantes = this.vacaciones.DiasTomados;
    const [año, mes, dia] = this.vacaciones.FechaInicio.split('-').map(Number);
    let fecha = new Date(año, mes - 1, dia);

    function aFechaISO(fecha: Date): string {
      const yyyy = fecha.getFullYear();
      const mm = String(fecha.getMonth() + 1).padStart(2, '0');
      const dd = String(fecha.getDate()).padStart(2, '0');
      return `${yyyy}-${mm}-${dd}`;
    }

    while (restantes > 0) {
      const iso = aFechaISO(fecha);
      const diaSemana = fecha.getDay();
      const esLaboral = diaSemana !== 0 && diaSemana !== 6 && !this.feriados.includes(iso);

      const yyyy = fecha.getFullYear();
      const mm = fecha.getMonth();
      const dd = fecha.getDate();

      if (esLaboral) {
        let mesExistente = this.meses.find(m => m.mes === mm && m.anio === yyyy);
        if (!mesExistente) {
          mesExistente = { mes: mm, anio: yyyy, dias: [] };
          this.meses.push(mesExistente);
        }
        mesExistente.dias.push(dd);
        this.ultimaFechaTomada = iso;
        restantes--;
      }

      fecha.setDate(fecha.getDate() + 1);
    }
    this.vacaciones.FechaFin = this.ultimaFechaTomada;
  }

  validarDiasTomados() {
    const maximo = 50;
    if (this.vacaciones.DiasTomados > maximo) {
      this.vacaciones.DiasTomados = maximo;
    }
  
    if (this.diasDisponibles !== null) {
      this.advertenciaDiasSuperados = this.vacaciones.DiasTomados > this.diasDisponibles;
    }
  
    this.actualizarCalendario();
  }

  obtenerNombreMes(mes: number): string {
    return new Date(2000, mes).toLocaleString('es-CL', { month: 'long' }).replace(/^\w/, c => c.toUpperCase());
  }

  actualizarDiasDisponibles() {
    const rut = this.vacaciones.RutTrabajador;
    const fecha = this.vacaciones.FechaInicio;
    if (!rut || !fecha) return;

    const anio = Number(fecha.split('-')[0]);

    this.http.get<{ DiasDisponibles: number }>(
      `http://127.0.0.1:8000/api/vacaciones/${rut}/dias-disponibles?anio=${anio}`
    ).subscribe({
      next: res => {
        this.diasDisponibles = res.DiasDisponibles;
      },
      error: err => {
        console.error('Error al obtener días disponibles:', err.error);
        this.diasDisponibles = null;
      }
    });
  }

  guardarVacaciones() {
    const id = this.route.snapshot.paramMap.get('id');
    const request = id
      ? this.http.put(`http://localhost:8000/api/vacaciones/${id}`, this.vacaciones)
      : this.http.post('http://localhost:8000/api/vacaciones/crear', this.vacaciones);

    request.subscribe({
      next: res => {
        console.log('Vacaciones guardadas:', res);
        this.router.navigate(['/vacaciones']);
      },
      error: err => {
        console.error('Error al guardar vacaciones:', err.error);
      }
    });
  }
  onDiasDisponiblesChange(dias: number) {
    this.diasDisponibles = dias;
    this.advertenciaDiasSuperados = this.vacaciones.DiasTomados > dias;
  }
}