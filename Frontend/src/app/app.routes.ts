import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { MenuComponent } from './pages/menu/menu.component';
import { CrearTrabajadoresComponent } from './pages/trabajadores/crear-trabajadores/crear-trabajadores.component';

export const routes: Routes = [
    { path: '', component: LoginComponent },
    { path: 'menu', component: MenuComponent },
    { path: 'trabajadores/crear', component: CrearTrabajadoresComponent },
];
