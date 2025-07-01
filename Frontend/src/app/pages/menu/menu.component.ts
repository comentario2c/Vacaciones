import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [RouterOutlet, CommonModule],
  templateUrl: './menu.component.html',
  styleUrl: './menu.component.css'
})
export class MenuComponent {
  sidebarVisible = false;

  constructor(public authService: AuthService) {}

  rolTienePermiso(roles: string | string[]): boolean {
    return this.authService.hasRole(roles);
  }

  toggleSidebar() {
    this.sidebarVisible = !this.sidebarVisible;
  }
}