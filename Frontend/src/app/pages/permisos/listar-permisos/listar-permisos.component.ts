import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Permiso } from '../../../shared/models/permisos.models';

@Component({
  selector: 'app-listar-permisos',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './listar-permisos.component.html',
  styleUrl: './listar-permisos.component.css'
})
export class ListarPermisosComponent {
  permisos: Permiso[] = []; 

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {
    this.http.get<Permiso[]>('http://127.0.0.1:8000/api/permisos')
      .subscribe({
        next: (data) => this.permisos = data,
        error: (err) => console.error('Error al obtener permisos', err)
      });
  }

  irACrearPermiso() {
    this.router.navigate(['/permisos/registrar']);
  }

  editarPermiso(id: number) {
    this.router.navigate(['/permisos/editar', id]);
  }

  eliminarPermiso(id: number) {
    this.http.delete(`http://127.0.0.1:8000/api/permisos/${id}`)
      .subscribe({
        next: () => this.ngOnInit(),
        error: (err) => console.error('Error al eliminar permiso', err)
      });
  }

  irAMenu() {
    this.router.navigate(['/menu']);
  }
}
