import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-listar-trabajadores',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './listar-trabajadores.component.html',
  styleUrl: './listar-trabajadores.component.css'
})
export class ListarTrabajadoresComponent {
  trabajadores: any[] = [];
  filtroNombre: string = '';

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {
    this.http.get<any[]>('http://127.0.0.1:8000/api/trabajadores')
      .subscribe({
        next: (data) => this.trabajadores = data,
        error: (err) => console.error('Error al obtener trabajadores', err)
      });
  }

    get trabajadoresFiltrados() {
    if (!this.filtroNombre) return this.trabajadores;
    return this.trabajadores.filter(t =>
      t.Nombre.toLowerCase().includes(this.filtroNombre.toLowerCase())
    );
  }

  irACrearTrabajador() {
    this.router.navigate(['/trabajadores/crear']);
  }

  editarTrabajador(rut: string) {
    this.router.navigate(['/trabajadores/editar', rut]);
  }

  eliminarTrabajador(rut: string) {
    this.http.delete(`http://127.0.0.1:8000/api/trabajadores/${rut}`)
      .subscribe({
        next: () => this.ngOnInit(),
        error: (err) => console.error('Error al eliminar trabajador', err)
      });
  }

  irAMenu() {
    this.router.navigate(['/menu']);
  }
}
