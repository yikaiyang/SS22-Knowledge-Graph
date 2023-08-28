import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Subject, from, of } from 'rxjs';
import { POI } from '../app/responses/poi-response';
import { Location } from '../app/responses/location';


@Injectable({
  providedIn: 'root'
})
export class MapService {

  locations$: Subject<Location[]> = new Subject()

  constructor() {
  }
}
