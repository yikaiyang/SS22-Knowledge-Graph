import { Component, OnInit } from '@angular/core';
import { MapService } from './map.service';
import { Observable as BehaviourSubject, Subject, of } from 'rxjs';
import { Location } from '../app/responses/location';
import { AppService } from '../app/app.service';

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

  selectedModel: any;

  tab_menu_options = ['Existing', 'Predictions']

  selected_tab_menu_option: any = this.tab_menu_options[0];

  onSelectTabMenuItem() {
    if (this.selected_tab_menu_option == this.tab_menu_options[0]) {
        // Existing
        this.onRelationshipChange()
    } else if (this.selected_tab_menu_option == this.tab_menu_options[1]) {
        // Predictions
        this.onRelationshipChange()
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

  selectedRelationship = this.relationships[0];



  selectedLocation: any = {};

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

  /** Related nodes */
  relationship_list: any =
    []

  onLoadRelatedNodes(location: Location) {
    if (this.selected_tab_menu_option == this.tab_menu_options[0]) {
      //Existing
      this.appService
      .getRelatedNodes(location.node_id, this.selectedRelationship)
      .subscribe((result) => {
        this.relationship_list = result
      })
    } else {
      // Using KGE models
      // Get model
      this.appService
      .getRelatedNodes(location.node_id, this.selectedRelationship, this.selectedModel)
      .subscribe((result) => {
        this.relationship_list = result
      })
    }
   
  }

  onTabSelect() {
    this.clearRelationshipList();

    // Load nodes related to node
    this.onLoadRelatedNodes(this.selectedLocation);
  }

  clearRelationshipList(): void {
    this.relationship_list = []
  }

  onRelationshipChange() {
    this.clearRelationshipList();

    // Load nodes related to node
    this.onLoadRelatedNodes(this.selectedLocation);
  }

  constructor(
    private mapService: MapService,
    private appService: AppService
  ) {
  }

  ngOnInit(): void {
    this.locations$ = this.mapService.locations$;
  }


  onItemClick(location: Location) {
    this.display = true;

    this.selectedLocation = location;
    console.log(location);

    this.clearRelationshipList();

    // Load nodes related to node
    this.onLoadRelatedNodes(this.selectedLocation);
  }

  display: boolean = true;

  showDialog() {
    this.display = true;
  }


  hasProp(o: any, name: any) {
    return o.hasOwnProperty(name);
  }

  isFinite(number: number): boolean {
    return Number.isFinite(number)
  }
}
