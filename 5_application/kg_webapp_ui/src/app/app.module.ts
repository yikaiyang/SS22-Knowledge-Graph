import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { OrderListModule } from 'primeng/orderlist';
import { NgxMapboxGLModule } from 'ngx-mapbox-gl';
import { MapComponent } from './map/map.component';
import { Button, ButtonModule } from 'primeng/button';
import { TabMenuModule } from 'primeng/tabmenu';
import {HttpClientModule} from '@angular/common/http';
import { ToolbarModule } from 'primeng/toolbar';
import { TooltipModule } from 'primeng/tooltip';
import { OverlayPanelModule } from 'primeng/overlaypanel';
import { DialogModule } from 'primeng/dialog';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { Listbox, ListboxModule } from 'primeng/listbox';
import { DropdownModule } from 'primeng/dropdown';
import { Chip, ChipModule } from 'primeng/chip';
import { SelectButtonModule } from 'primeng/selectbutton';
import {PanelModule} from 'primeng/panel';
import { FormsModule } from '@angular/forms';
import {Divider, DividerModule} from 'primeng/divider';
import { TagModule } from 'primeng/tag';
import { Slider, SliderModule } from 'primeng/slider';
import {InputTextModule } from 'primeng/inputtext';
import {CheckboxModule} from 'primeng/checkbox';


const TOKEN = 'pk.eyJ1IjoieWlrYWl5YW5nIiwiYSI6ImNqaXJ5eXd6MDBhOGwzcGxvMmUwZGxsaDkifQ.Czx2MTe4B6ynlMbpW52Svw'

@NgModule({
  declarations: [
    AppComponent,
    MapComponent
  ],
  imports: [
    CheckboxModule,
    InputTextModule,
    SliderModule,
    ChipModule,
    DividerModule,
    SelectButtonModule,
    BrowserModule,
    PanelModule,
    FormsModule,
    ListboxModule,
    DropdownModule,
    OrderListModule,
    TagModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    ToolbarModule,
    ButtonModule,
    TabMenuModule,
    HttpClientModule,
    TooltipModule,
    DialogModule,
    OverlayPanelModule,
    NgxMapboxGLModule.withConfig({
      accessToken: TOKEN, // Optional, can also be set per map (accessToken input of mgl-map)
    })
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
