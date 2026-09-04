import { Component,ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class LoginComponent {

  email = '';
  password = '';
  loading = false;
  error = '';
  

  apiUrl = 'https://ai-sd-security-analyzer.onrender.com';

  constructor(private http: HttpClient, private router: Router) {}

  login() {
    console.log('LoginComponent initialized');
    this.loading = true;
    this.error = '';

    this.http.post(`${this.apiUrl}/auth/login`, {
      email: this.email,
      password: this.password
    }).subscribe({
      next: (res: any) => {
        localStorage.setItem('token', res.access_token); // store token
        this.router.navigate(['/analyze']); // 🔥 Navigate on success
      },
      error: () => {
        console.log('err',this.error)
        this.error = 'Invalid credentials';
        this.loading = false;
      }
    });
  }
}