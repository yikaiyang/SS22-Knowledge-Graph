import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  constructor(private httpClient: HttpClient) { }
  
  loadPOIs() {
    this.httpClient.get('http://localhost:8000/poi/').subscribe((result) => {
      console.log(result)
    })
  }
}
