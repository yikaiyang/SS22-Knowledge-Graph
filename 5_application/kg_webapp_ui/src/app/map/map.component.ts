import { Component, OnInit } from '@angular/core';
import { MapService } from './map.service';
import { Observable as BehaviourSubject, Subject, of } from 'rxjs';
import { Location } from '../app/responses/location';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {

  models = [
    'TransE',
    'TransD',
    'TransH',
    'RotatE',
  ]

  tab_menu_options = ['Existing', 'Predictions']

  selected_tab_menu_option = this.tab_menu_options[0]

  onSelectTabMenuItem() {
    if (this.selected_tab_menu_option == this.tab_menu_options[0]) {

    } else if (this.selected_tab_menu_option == this.tab_menu_options[1]) {
      
    }
  }

  relationships = [
    'IS_CONNECTED',
    'IS_LOCATED',
    'IS_NEARBY',
    'HAS_INCIDENT',
    'HAS_TEMPERATURE',
    'HAS_WEATHER',
    'HAS_TRAFFIC_SITUATION'
  ]

  selectedRelationship = '';

  selectedLocation$ = new Subject<Location>();

  locations$: BehaviourSubject<Location[]> = of(
    [
    {
      "node_id": "5cf54e0d8af84867a651f58079be05f5",
      "latitude": 48.216403322294354,
      "longitude": 16.341783329844475,
      "length": 41,
      "name": "Innerer Gürtel-41"
    }
  ]
  )

  constructor(
    private mapService: MapService
  ) {
  }

  ngOnInit(): void {
    this.locations$ = this.mapService.locations$;
  }


  onItemClick(location: Location) {
    this.display = true;
    this.selectedLocation$.next(location);
  }

  display: boolean = true;

  showDialog() {
    this.display = true;
  }
}
