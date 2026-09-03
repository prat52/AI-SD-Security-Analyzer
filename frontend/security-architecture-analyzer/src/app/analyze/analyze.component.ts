

import { Component } from '@angular/core';
import { AnalysisService } from '../services/analysis.service';
import { Router } from '@angular/router';


interface Finding {
  title: string;
  severity: string;
  stride: string;
  owasp: string;
  mitre: string[];
  recommendation: string;
}



interface AnalysisResponse {
  findings: Finding[];
}

@Component({
  selector: 'app-analyze',
  templateUrl: './analyze.component.html',
  styleUrls: ['./analyze.component.scss']
  
})
export class AnalyzeComponent {


  

  private severityOrder: Record<string, number> = {
  CRITICAL: 4,
  HIGH: 3,
  MEDIUM: 2,
  LOW: 1
};

architectures: any[] = [];

  logout() {
    localStorage.removeItem('token');  // Remove JWT
    this.router.navigate(['/login']);  // Redirect
  }


loadArchitectures() {

  const token = localStorage.getItem('token');

  fetch('http://localhost:8000/architectures', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  .then(res => res.json())
  .then(data => {

    data.forEach((arch: any) => {

      if (typeof arch.response === 'string') {
        arch.response = JSON.parse(arch.response);
      }

    });

    this.architectures = data;

  })
  .catch(err => {
    console.error(err);
  });

}

  architectureText = '';
  result: AnalysisResponse | null = null;
  loading = false;

  constructor(private analysisService: AnalysisService, private router: Router) {}

  analyze() {
    if (!this.architectureText.trim()) return;

    this.loading = true;
    this.result = null;

    this.analysisService.analyzeArchitecture(this.architectureText)
      .subscribe({
        next: (res: any) => {
  this.result = res;  // ← res.response is now a dict with findings
  if (this.result?.findings) {
    this.result.findings.sort(
      (a, b) => this.severityOrder[b.severity] - this.severityOrder[a.severity]
    );
  }
  this.loading = false;
},
        error: (err) => {
          console.error('Full error:', err.error);
          this.loading = false;
        }
      });
  }
}
