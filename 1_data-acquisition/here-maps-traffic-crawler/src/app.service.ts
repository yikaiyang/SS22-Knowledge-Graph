import { HttpService } from '@nestjs/axios';
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { Observable, repeat, tap } from 'rxjs';
import * as fs from 'fs';
import { stringify } from 'csv-stringify';

@Injectable()
export class AppService {

  private URL: string = 'https://data.traffic.hereapi.com/v7/flow?in=corridor:BF-usmJsw6jDyD8b7gBiQ_T0X7bsF7W4Z_YuV_JgsBoJiejC2nBzXkRtaoDtQmgBtG-c_YyWhjB53BhenhBuLvWY3lCpOtyBlRvzB3P1nBnEvkB2F5awVhQyXpTVtUyS1KwayI4jBxI8gBrF4U0JqToD8biQua8MuQieukByI4Pie;r=200&locationReferencing=shape&apiKey=';

  constructor(
    private httpService: HttpService,
    private configService: ConfigService
  ) {
    const apiKey = this.configService.get('API_KEY');
    // Set API KEY
    this.URL = `${this.URL}${apiKey}`;
    //let path = __dirname + '/data.csv';
    let path = '/data/data.csv'
    this.getTrafficInfo().pipe(
      tap((response) => {
        this.writeToCSV(path,
          [{
            "Timestamp": response?.data?.sourceUpdated,
            "Data": response?.data?.results
          }]
        );
        console.log(`${new Date().toISOString()} Retrieved: ${response}`);
      }),
      repeat({
        delay: 60000 * 20// 1 minute
      })
    ).subscribe()
    console.log(this.URL);
  }

  writeToCSV(path: string, data: any) {
    if (!fs.existsSync(path)) {
      console.log(`${new Date().toISOString()}: File ${path} does not exist: Creating file`)
      stringify(data, {header: true}, (err, output) => {
        fs.writeFileSync(path, output);
      })
    } else {
      console.log(`${new Date().toISOString()}: File ${path} exists: Append data to file`)
      stringify(data, {header: false}, (err, output) => {
        fs.appendFileSync(path, output);
      })
    }   
  }

  getTrafficInfo(): Observable<any> {
    console.log(`${new Date().toISOString()} Request sent`);
    return this.httpService.get(this.URL);
  }
}
