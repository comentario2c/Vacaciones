import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
import { Permiso } from '../../../shared/models/permisos.models';
import { DiasdisponiblesComponent } from '../../vacaciones/diasdisponibles/diasdisponibles.component';
import { CalendarioComponent } from '../../vacaciones/calendario/calendario.component';

@Component({
  selector: 'app-registrar-permisos',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule, DiasdisponiblesComponent, CalendarioComponent],
  templateUrl: './registrar-permisos.component.html',
  styleUrl: './registrar-permisos.component.css'
})
export class RegistrarPermisosComponent {
  permisos: Permiso = {
    ID_Permiso: 0,
    RutTrabajador: '',
    NombreTrabajador: '',
    FechaInicio: '',
    FechaFin: '',
    DiasTomados: 0,
    ConCargoVacaciones: false,
    Motivo: ''
  }; 

  trabajadores: { Nombre: string; RutTrabajador: string }[] = [];
  busqueda: string = '';
  trabajadorSeleccionado: string = '';

  diasMesActual: number[] = [];
  diasMesSiguiente: number[] = [];
  ultimaFechaTomada: string = '';
  meses: { mes: number; anio: number; dias: number[] }[] = [];
  feriados: string[] = [];

  diasDisponibles: number | null = null;
  anioConsulta: number | null = null;

  constructor(private http: HttpClient, private router: Router, private route: ActivatedRoute) {}

  ngOnInit() {
    // 1. Primero cargar feriados
    this.http.get<string[]>('http://localhost:8000/api/vacaciones/feriados')
      .subscribe(f => this.feriados = f);

    // 2. Luego cargar trabajadores y si hay ID, cargar vacaciones
    this.cargarTrabajadores().then(() => {
      const id = this.route.snapshot.paramMap.get('id');
      if (id) {
        this.http.get<Permiso>(`http://localhost:8000/api/permisos/${id}`).subscribe({
          next: data => {
            this.permisos = data;

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

  crearPermiso() {
    console.log('Datos que se enviarán al backend:', this.permisos);
    this.http.post('http://127.0.0.1:8000/api/permisos/crear', this.permisos).subscribe({
      next: (response) => {
      console.log('Permiso registrado:', response);
      this.router.navigate(['/permisos']);
    },
    error: (err: any) => {
      console.error('Error al crear permiso:', err.error);
    }
  });
  }

  obtenerNombreMes(mes: number): string {
    return new Date(2000, mes).toLocaleString('es-CL', { month: 'long' }).replace(/^\w/, c => c.toUpperCase());
  }

  validarDiasTomados() {
    const maximo = 50;
    if (this.permisos.DiasTomados > maximo) {
      this.permisos.DiasTomados = maximo;
    }
    this.actualizarCalendario();
  }


  actualizarCalendario() {
    if (!this.permisos.FechaInicio || !this.permisos.DiasTomados) return;

    this.meses = [];
    this.diasMesActual = [];
    this.diasMesSiguiente = [];

    let restantes = this.permisos.DiasTomados;
    const [año, mes, dia] = this.permisos.FechaInicio.split('-').map(Number);
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
    this.permisos.FechaFin = this.ultimaFechaTomada;
  }

  actualizarDiasDisponibles() {
    const rut = this.permisos.RutTrabajador;
    const fecha = this.permisos.FechaInicio;
    if (!rut || !fecha) return;

    const anio = Number(fecha.split('-')[0]);

    this.http.get<{ total_a_planificar: number }>(
      `http://127.0.0.1:8000/api/calculos/saldo-completo/${rut}/${anio}`
    ).subscribe({
      next: res => {
        this.diasDisponibles = res.total_a_planificar;
      },
      error: err => {
        console.error('Error al obtener días disponibles:', err.error);
        this.diasDisponibles = null;
      }
    });
  }

  seleccionarTrabajador(nombre: string) {
    const trabajador = this.trabajadores.find(t => t.Nombre === nombre);
    if (trabajador) {
      this.permisos.RutTrabajador = trabajador.RutTrabajador;
      this.trabajadorSeleccionado = trabajador.Nombre;
      this.busqueda = trabajador.Nombre;
      this.actualizarDiasDisponibles();
    }
  }

  esNombreExacto(nombre: string): boolean {
    return this.trabajadores.some(t => t.Nombre.toLowerCase() === nombre.toLowerCase());
  }

  get trabajadoresFiltrados() {
    const termino = this.busqueda?.toLowerCase() ?? '';
    return this.trabajadores.filter(t =>
      t.Nombre.toLowerCase().includes(termino)
    );
  }

  guardarPermiso() {
    const id = this.route.snapshot.paramMap.get('id');
    const request = id
      ? this.http.put(`http://localhost:8000/api/permisos/${id}`, this.permisos)
      : this.http.post('http://localhost:8000/api/permisos/crear', this.permisos);

    request.subscribe({
      next: res => {
        console.log('Permiso guardado:', res);
        this.router.navigate(['/permisos']);
      },
      error: err => {
        console.error('Error al guardar permisos:', err.error);
      }
    });
  }
}
