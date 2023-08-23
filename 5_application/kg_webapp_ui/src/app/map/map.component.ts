import { Component, OnInit } from '@angular/core';
import { MapService } from './map.service';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {


  locations: any[] = []

  constructor(private mapService: MapService) {
    this.locations = this.mapService.locations;
  }

  ngOnInit(): void {
  }

}
