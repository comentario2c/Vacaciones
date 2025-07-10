import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { VacacionesEditar } from '../../../shared/models/vacaciones.models';

@Component({
  selector: 'app-editar-vacaciones',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './editar-vacaciones.component.html',
  styleUrl: './editar-vacaciones.component.css'
})
export class EditarVacacionesComponent {
  vacaciones: VacacionesEditar = {
    ID_Movimiento: 0,
    RutTrabajador: '',
    FechaInicio: '',
    FechaFin: '',
    DiasTomados: 0,
    Observaciones: ''
  };

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private router: Router
  ) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.http.get<VacacionesEditar>(`http://localhost:8000/api/vacaciones/${id}`)
        .subscribe(v => this.vacaciones = v);
    }
  }

  actualizarVacaciones() {
    if (!this.vacaciones.ID_Movimiento) return;

    this.http.put(`http://localhost:8000/api/vacaciones/${this.vacaciones.ID_Movimiento}`, this.vacaciones)
      .subscribe({
        next: () => this.router.navigate(['/vacaciones']),
        error: err => console.error('Error al actualizar:', err.error)
      });
  }
}
