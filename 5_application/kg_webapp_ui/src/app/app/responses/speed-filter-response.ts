import { Location } from "./location"

export interface SpeedFilterResponse {
    response: Response
  }
  
  export interface Response {
    status: string
    data: Data[]
  }
  
  export interface Data {
    node_properties: Location
  }
  