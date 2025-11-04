import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login';


export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  {
    path: 'dashboard',
    loadComponent: () =>
      import('./pages/dashboard/dashboard').then(
        (m) => m.DashboardComponent
      ),
  },
{
  path: 'milk-supply',
  loadComponent: () =>
    import('./pages/milk-supply/milk-supply').then(
      (m) => m.MilkSupplyComponent
    ),
}

];
