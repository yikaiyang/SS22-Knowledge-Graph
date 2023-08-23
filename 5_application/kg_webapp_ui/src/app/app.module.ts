import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { NgxMapboxGLModule } from 'ngx-mapbox-gl';
import { MapComponent } from './map/map.component';
import { Button, ButtonModule } from 'primeng/button';
import { TabMenuModule } from 'primeng/tabmenu';
import {HttpClientModule} from '@angular/common/http';

const TOKEN = 'pk.eyJ1IjoieWlrYWl5YW5nIiwiYSI6ImNqaXJ5eXd6MDBhOGwzcGxvMmUwZGxsaDkifQ.Czx2MTe4B6ynlMbpW52Svw'

@NgModule({
  declarations: [
    AppComponent,
    MapComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ButtonModule,
    TabMenuModule,
    HttpClientModule,
    NgxMapboxGLModule.withConfig({
      accessToken: TOKEN, // Optional, can also be set per map (accessToken input of mgl-map)
    })
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
