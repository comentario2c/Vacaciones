import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-crear-trabajadores',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './crear-trabajadores.component.html',
  styleUrl: './crear-trabajadores.component.css'
})
export class CrearTrabajadoresComponent {
  trabajador = {
    rut: '',
    nombre: '',
    fechaContrato: ''
  };

  constructor(private http: HttpClient) {}
  
  crearTrabajador() {
    this.http.post('http://localhost:8000/api/trabajadores', this.trabajador).subscribe((response) => {
      console.log('Trabajador creado:', response);
    });
  }
}
