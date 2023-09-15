import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, map } from 'rxjs';
import { POIResponse, POI } from './responses/poi-response';
import { IncidentResponse, Incident } from './responses/incident-response';
import { Road, RoadResponse } from './responses/road-response';
import { Location, RelatedNodeResponse } from './responses/related_node-response';
import { SpeedFilterResponse } from './responses/speed-filter-response';
import { Date, DateResponse } from './responses/date-response';
import { Time, TimeResponse } from './responses/time-response';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  isTrafficSpeedFilterActive$ = new BehaviorSubject(false);

  active_category$ = new BehaviorSubject('');

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

  getSpeedFilterReponse(node_type: string, start_range: number, end_range: number, date: string, time: string) {
    return this.httpClient
      .get<SpeedFilterResponse>(`http://localhost:8000/speed?range_start=${start_range}&range_end=${end_range}&node_type=${node_type}&date=${date}&time=${time}`)

  }

  getSpeedFilter(node_type: string, start_range: number, end_range: number, date: string, time: string) {
    return this.getSpeedFilterReponse(node_type, start_range, end_range, date, time)
      .pipe(map(response =>
        response.response.data.map(data => data.node_properties)
      )
      );
  }

  getTimeResponse(): Observable<TimeResponse> {
    return this.httpClient.get<TimeResponse>('http://localhost:8000/time')
  }

  getTime(): Observable<Time[]> {
    return this.getTimeResponse()
      .pipe(map(response =>
        response.response.data.map(data => data.node_properties)
      )
      );
  }

  getDateResponse(): Observable<DateResponse> {
    return this.httpClient.get<DateResponse>('http://localhost:8000/date')
  }

  getDate(): Observable<Date[]> {
    return this.getDateResponse()
      .pipe(map(response =>
        response.response.data.map(data => data.node_properties)
      )
      );
  }

}
