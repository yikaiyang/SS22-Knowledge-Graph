import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { POIResponse, POI } from './responses/poi-response';
import { IncidentResponse, Incident} from './responses/incident-response';
import { Road, RoadResponse } from './responses/road-response';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  

  constructor(private httpClient: HttpClient) { }
  
  getPOIsResponse(): Observable<POIResponse> {
    return this.httpClient.get<POIResponse>('http://localhost:8000/poi/')
  }

  getPOIs(): Observable<POI[]> {
    return this.getPOIsResponse().pipe(
      map(response => 
        response.response.data.map(data => data.node_properties)
      )
    )
  }

  getIncidentsResponse(): Observable<IncidentResponse> {
    return this.httpClient.get<IncidentResponse>('http://localhost:8000/incident/')
  }

      
  getIncidents(): Observable<Incident[]> {
   return this.getIncidentsResponse().pipe(
      map(response => 
        response.response.data.map(data => data.node_properties))
    )
  }

  getRoadsResponse(): Observable<RoadResponse> {
    return this.httpClient.get<RoadResponse>('http://localhost:8000/road/')
  }

      
  getRoads(): Observable<Road[]> {
   return this.getRoadsResponse().pipe(
      map(response => 
        response.response.data.map(data => data.node_properties))
    )
  }

}
