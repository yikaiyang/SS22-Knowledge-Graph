import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';


export interface Location {
  latitude: number,
  longitude: number,
  name: string,
  type: string
}

@Injectable({
  providedIn: 'root'
})
export class MapService {

  locations: Location[] = [{ 
    latitude: 48.21, 
    longitude: 16.36,
    name: 'Location',
    type: 'Unknown'
  }]

  constructor() { 
  }
}
