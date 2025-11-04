import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-milk-supply',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './milk-supply.html',
  styleUrl: './milk-supply.css',
})
export class MilkSupplyComponent {
date = '';
  liters: number | null = null;
  rate: number | null = null;
  loading = false;
  message = '';
  list: any[] = [];

  private apiUrlAdd = 'https://glorious-umbrella-xqpgr767g73qr7-5000.app.github.dev/api/milk';       // adjust if your endpoint path differs
  private apiUrlList = 'https://glorious-umbrella-xqpgr767g73qr7-5000.app.github.dev/api/milk';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadList();
  }

  saveSupply() {
    if (!this.date || !this.liters || !this.rate) {
      this.message = 'Please fill all fields';
      return;
    }
    this.loading = true;
    this.http.post<any>(`${this.apiUrlAdd}`, {
      date: this.date,
      liters: this.liters,
      rate: this.rate
    }).subscribe({
      next: (res) => {
        this.loading = false;
        if (res.success) {
          this.message = '✅ Supply recorded successfully';
          this.date = '';
          this.liters = null;
          this.rate = null;
          this.loadList();
        } else {
          this.message = res.message || 'Failed to record supply';
        }
      },
      error: (err) => {
        this.loading = false;
        this.message = err.error?.message || 'Error connecting to server';
      }
    });
  }

  loadList() {
    this.http.get<any>(`${this.apiUrlList}`).subscribe({
      next: (res) => {
        if (res.success === false) {
          this.list = [];
          this.message = res.message || '';
        } else {
          this.list = res.data || res;       // depends on API response structure
        }
      },
      error: (err) => {
        this.list = [];
        this.message = 'Could not load list';
      }
    });
  }
}
