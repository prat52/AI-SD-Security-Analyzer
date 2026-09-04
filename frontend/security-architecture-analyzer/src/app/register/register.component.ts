import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent {
  name = '';
  email = '';
  password = '';
  loading = false;
  error = '';
  success = '';

  apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient, private router: Router) {}

  register() {
    this.loading = true;
    this.error = '';
    this.success = '';

    this.http.post(`${this.apiUrl}/auth/register`, { 
      email: this.email,
      password: this.password
    }).subscribe({
      next: () => {
        this.success = 'Registration successful! Redirecting...';
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 1500);
      },
      error: (err) => {
        console.log(err)
        this.error = 'Registration failed';
        this.loading = false;
      }
    });
  }
}