import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient,HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
templateUrl: './login.html',
  styleUrl: './login.css',
})
export class LoginComponent {
  username = '';
  password = '';
  loading = false;
  errorMessage = '';

  private apiUrl = 'https://glorious-umbrella-xqpgr767g73qr7-5000.app.github.dev/api/auth/login'; // Flask backend

  constructor(private http: HttpClient, private router: Router) {}

  login() {
    this.loading = true;
    this.errorMessage = '';

    this.http
      .post<any>(this.apiUrl, {
        username: this.username,
        password: this.password,
      })
      .subscribe({
        next: (res) => {
          this.loading = false;
          localStorage.setItem('user', JSON.stringify(res.user));
          this.router.navigate(['/dashboard']);
        },
        error: (err) => {
          this.loading = false;
          this.errorMessage =
            err.error?.message || 'Invalid username or password';
        },
      });
  }
}
