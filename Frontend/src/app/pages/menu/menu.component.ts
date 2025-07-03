import { Component } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../core/services/auth.service';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [RouterOutlet, CommonModule, RouterModule],
  templateUrl: './menu.component.html',
  styleUrl: './menu.component.css'
})
export class MenuComponent {
  sidebarVisible = false;

  constructor(public authService: AuthService, private router: Router) {}

  rolTienePermiso(roles: string | string[]): boolean {
    return this.authService.hasRole(roles);
  }

  toggleSidebar() {
    this.sidebarVisible = !this.sidebarVisible;
  }

  irTrabajadores() {
    this.router.navigate(['/trabajadores']);
  }
}