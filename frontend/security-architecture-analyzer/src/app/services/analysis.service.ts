// import { Injectable } from '@angular/core';
// import { HttpClient } from '@angular/common/http';

// @Injectable({
//   providedIn: 'root'
// })
// export class AnalysisService {

//   private API_URL = 'http://localhost:8000/api/analyze';

//   constructor(private http: HttpClient) {}

//   analyzeArchitecture(architectureText: string) {
//     return this.http.post<any>(this.API_URL, {
//       architecture_text: architectureText
//     });
//   }
// }

import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AnalysisService {

  private API_URL = 'http://localhost:8000/api/analyze'; 
  // make sure this matches your backend route

  constructor(private http: HttpClient) {}

  analyzeArchitecture(architectureText: string) {

    const token = localStorage.getItem('token');

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json'
    });

    return this.http.post<any>(
      this.API_URL,
      { architecture_text: architectureText },   // match backend field name
      { headers }
    );
  }
}
