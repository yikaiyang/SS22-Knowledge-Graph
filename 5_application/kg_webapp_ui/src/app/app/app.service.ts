import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { POIResponse, POI } from './responses/poi-response';
import { IncidentResponse, Incident} from './responses/incident-response';
import { Road, RoadResponse } from './responses/road-response';
import { Location, RelatedNodeResponse } from './responses/related_node-response';

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
  

  getRelatedNodesResponse(nodeId: string, relationship: string, prediction_model?: string): Observable<RelatedNodeResponse> {
    if (prediction_model != null) {
      return this.httpClient
        .get<RelatedNodeResponse>(`http://localhost:8000/nodes?id=${nodeId}&r=${relationship}&p=${prediction_model}`)
    } else {
      return this.httpClient
        .get<RelatedNodeResponse>(`http://localhost:8000/nodes?id=${nodeId}&r=${relationship}`)
    }
  }

  getRelatedNodes(nodeId: string, relationship: string, prediction_model?: string): Observable<Location[]> {
    return this.getRelatedNodesResponse(nodeId, relationship, prediction_model)
      .pipe(map(response => 
        response.response.data.map(data => data.node_properties)
        )
      )
  }

}
