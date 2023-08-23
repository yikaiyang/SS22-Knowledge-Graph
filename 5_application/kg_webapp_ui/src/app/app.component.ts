import { Component } from '@angular/core';
import { MenuItem } from 'primeng/api';
import { Subject } from 'rxjs';
import { AppService } from './app/app.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'kg_webapp_ui';

  categories = [
    { label: 'POI' },
    { label: 'Streets' },
    { label: 'Incidents' },
  ];

  active_category: any = null

  constructor(private appService: AppService) {
  }

  ngOnInit() {
    this.active_category = this.categories[0]
  }

  onTabItemClick(i: any) {
    console.log(this.categories[i].label)
    switch (i) {
      case 0:
        // POIs
        this.appService.loadPOIs()
    }
  }

}
