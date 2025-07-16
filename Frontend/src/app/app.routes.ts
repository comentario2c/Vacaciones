import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { MenuComponent } from './pages/menu/menu.component';

// Trabajadores
import { CrearTrabajadoresComponent } from './pages/trabajadores/crear-trabajadores/crear-trabajadores.component';
import { ListarTrabajadoresComponent } from './pages/trabajadores/listar-trabajadores/listar-trabajadores.component';
import { EditarTrabajadoresComponent } from './pages/trabajadores/editar-trabajadores/editar-trabajadores.component';

// Vacaciones
import { RegistrarVacacionesComponent } from './pages/vacaciones/registrar-vacaciones/registrar-vacaciones.component';
import { ListarVacacionesComponent } from './pages/vacaciones/listar-vacaciones/listar-vacaciones.component';
import { CalendarioCompletoComponent } from './pages/reportes/calendario-completo/calendario-completo.component';
import { RegistrarPermisosComponent } from './pages/permisos/registrar-permisos/registrar-permisos.component';
import { ListarPermisosComponent } from './pages/permisos/listar-permisos/listar-permisos.component';

export const routes: Routes = [
    { path: '', component: LoginComponent },
    { path: 'menu', component: MenuComponent },

    // Trabajadores
    { path: 'trabajadores/crear', component: CrearTrabajadoresComponent },
    { path: 'trabajadores', component: ListarTrabajadoresComponent },
    { path: 'trabajadores/editar/:rut', component: EditarTrabajadoresComponent },

    // Vacaciones
    { path: 'vacaciones', component: ListarVacacionesComponent },
    { path: 'vacaciones/registrar', component: RegistrarVacacionesComponent},
    { path: 'vacaciones/editar/:id', component: RegistrarVacacionesComponent},

    // Permisos
    { path: 'permisos', component: ListarPermisosComponent },
    { path: 'permisos/registrar', component: RegistrarPermisosComponent },
    { path: 'permisos/editar/:id', component: RegistrarPermisosComponent },

    // Reportes
    { path: 'reportes/calendario-completo', component: CalendarioCompletoComponent },
];
