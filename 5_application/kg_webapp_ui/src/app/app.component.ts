import { Component } from '@angular/core';
import { MenuItem } from 'primeng/api';
import { Subject, Subscription, tap } from 'rxjs';
import { AppService } from './app/app.service';
import { MapService } from './map/map.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'kg_webapp_ui';

  sub: Subscription | null = null;




  categories = [
    { label: 'POI' },
    { label: 'Streets' },
    { label: 'Incidents' },
  ];

  active_category: any = null

  constructor(
    private appService: AppService,
    private mapService: MapService
  ) {
  }

  ngOnInit() {
    this.active_category = this.categories[0]
  }

  ngOnDestroy() {
    this.sub?.unsubscribe()
  }

  onTabItemClick(i: any) {
    console.log(this.categories[i].label)
    switch (i) {
      case 0:
        // POIs
        this.sub = this.appService.getPOIs().pipe(
          tap((res) => {
            console.log('http request')
            this.mapService.locations$.next(res)
          })
        ).subscribe();

        break;
      case 1:
        // Streets
        this.sub = this.appService.getRoads().pipe(
          tap((res) => {
            console.log('http request')
            this.mapService.locations$.next(res)
          })
        ).subscribe();
        break;
      case 2:
        // Incidents
        this.sub = this.appService.getIncidents().pipe(
          tap((res) => {
            console.log('http request')
            this.mapService.locations$.next(res)
          })
        ).subscribe();
        break;
    }
  }


}
