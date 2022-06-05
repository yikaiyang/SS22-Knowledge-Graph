import { HttpService } from '@nestjs/axios';
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { Observable, repeat, tap } from 'rxjs';
import * as fs from 'fs';
import { stringify } from 'csv-stringify';

@Injectable()
export class AppService {

  constructor(
    private httpService: HttpService,
    private configService: ConfigService
  ) {
    // Set API KEY
    let URL = this.configService.get(`URL`);
    let INTERVAL = this.configService.get(`INTERVAL`);
    //let path = __dirname + '/data.csv';
    let path = '/data/data.csv';
    this.getResponse(URL).pipe(
      tap((response) => {
        this.writeToCSV(path,
          [{
            "Timestamp": new Date().toISOString(),
            "Data": JSON.stringify(response?.data)
          }]
        );
        console.log(`${new Date().toISOString()} Retrieved: ${response?.data}`);
      }),
      repeat({
        delay: 360000 // in ms
      })
    ).subscribe()
    console.log(URL);
  }

  writeToCSV(path: string, data: any) {
    if (!fs.existsSync(path)) {
      console.log(`${new Date().toISOString()}: File ${path} does not exist: Creating file`)
      stringify(data, {header: true, delimiter: ';'}, (err, output) => {
        fs.writeFileSync(path, output);
      })
    } else {
      console.log(`${new Date().toISOString()}: File ${path} exists: Append data to file`)
      stringify(data, {header: false, delimiter: ';'}, (err, output) => {
        fs.appendFileSync(path, output);
      })
    }   
  }

  getResponse(URL: string): Observable<any> {
    console.log(`${new Date().toISOString()} Request sent`);
    return this.httpService.get(URL);
  }
}
