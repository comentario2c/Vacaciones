import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-listar-vacaciones',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './listar-vacaciones.component.html',
  styleUrl: './listar-vacaciones.component.css'
})
export class ListarVacacionesComponent {
  vacaciones: any[] = [];

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {
    this.http.get<any[]>('http://localhost:8000/api/vacaciones').subscribe(vacaciones => {
      this.vacaciones = vacaciones;
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
