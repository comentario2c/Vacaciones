import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { Trabajador } from '../../../shared/models/trabajador.models';

@Component({
  selector: 'app-editar-trabajadores',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './editar-trabajadores.component.html',
  styleUrls: ['./editar-trabajadores.component.css']
})
export class EditarTrabajadoresComponent {
  trabajador: Trabajador = {
    RutTrabajador: '',
    Nombre: '',
    Cargo: '',
    FechaContrato: ''
  };

  constructor(
    private http: HttpClient,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    const rut = this.route.snapshot.paramMap.get('rut');
    if (rut) {
      this.http.get<Trabajador>(`http://127.0.0.1:8000/api/trabajadores/${rut}`).subscribe((data) => {
        this.trabajador = data;
      });
    }
  }

  editarTrabajador() {
    this.http.put(`http://127.0.0.1:8000/api/trabajadores/${this.trabajador.RutTrabajador}`, this.trabajador).subscribe(() => {
      this.router.navigate(['/trabajadores']);
    });
  }
}
