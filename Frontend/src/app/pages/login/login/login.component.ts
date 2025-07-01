import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, HttpClientModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  email = '';
  password = '';

  constructor(private http: HttpClient) {}

  onSubmit() {
    console.log('Email:', this.email);
    console.log('Password:', this.password);
    this.http.post('http://localhost:8000/api/auth/login', {
      email: this.email,
      password: this.password
    }).subscribe((response) => {
      console.log('Respuesta del servidor:', response);
    });
  }
}