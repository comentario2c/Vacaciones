import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { Trabajador } from '../../../shared/models/trabajador.models';

@Component({
  selector: 'app-crear-trabajadores',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './crear-trabajadores.component.html',
  styleUrl: './crear-trabajadores.component.css'
})
export class CrearTrabajadoresComponent {
  trabajador: Trabajador = {
    Nombre: '',
    RutTrabajador: '',
    Cargo: '',
    FechaContrato: '',
    AnosRestantes: 0,
    SaldoVacaciones: 0
  };

  constructor(private http: HttpClient, private router: Router) {}

  crearTrabajador() {
    console.log('Datos que se enviarán al backend:', this.trabajador);
    this.http.post('http://127.0.0.1:8000/api/trabajadores/crear', this.trabajador).subscribe({
      next: (response) => {
      console.log('Trabajador creado:', response);
      this.router.navigate(['/trabajadores']);
    },
    error: (err: any) => {
      console.error('Error al crear trabajador:', err.error);
    }
  });
  }
}
