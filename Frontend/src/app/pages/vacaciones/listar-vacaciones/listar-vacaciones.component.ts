import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-listar-vacaciones',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './listar-vacaciones.component.html',
  styleUrl: './listar-vacaciones.component.css'
})
export class ListarVacacionesComponent {
  vacaciones: any[] = [];
  filtroNombre: string = '';
  filtroAnio: string | number = '';

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {
    this.http.get<any[]>('http://localhost:8000/api/vacaciones').subscribe(vacaciones => {
      this.vacaciones = vacaciones;
    });
  }

  get vacacionesFiltradas() {
    const anioFiltro = (this.filtroAnio === '' || this.filtroAnio == null)
      ? null
      : Number(this.filtroAnio);               // normalizamos a number

    return this.vacaciones.filter(v => {
      // filtro por nombre (ignora case)
      const nombre = (v.NombreTrabajador ?? '').toString();
      const coincideNombre = !this.filtroNombre
        || nombre.toLowerCase().includes(this.filtroNombre.toLowerCase());

      // extraer año de FechaInicio de forma segura
      let anioInicio: number | null = null;
      if (v.FechaInicio) {
        const d = new Date(v.FechaInicio);
        if (!isNaN(d.getTime())) {
          anioInicio = d.getFullYear();
        }
      }

      // si anioFiltro es null => aceptar todos; si no => comparar numéricamente
      const coincideAnio = anioFiltro == null || anioInicio === anioFiltro;

      return coincideNombre && coincideAnio;
    });
  }

  eliminarVacacion(id: number) {
    this.http.delete(`http://localhost:8000/api/vacaciones/${id}`).subscribe({
      next: res => {
        console.log('Vacación eliminada:', res);
        this.vacaciones = this.vacaciones.filter(v => v.id !== id);
      },
      error: err => {
        console.error('Error al eliminar vacación:', err.error);
      }
    });
  }

  editarVacacion(id: number) {
    this.router.navigate(['/vacaciones/editar', id]);
  }

  irACrearVacacion() {
    this.router.navigate(['/vacaciones/registrar']);
  }

  irAMenu() {
    this.router.navigate(['/menu']);
  }
}
