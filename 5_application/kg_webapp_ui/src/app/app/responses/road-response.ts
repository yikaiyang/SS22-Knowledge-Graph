export interface RoadResponse {
    response: Response
  }
  
  export interface Response {
    status: string
    data: Data[]
  }
  
  export interface Data {
    node_properties: Road
  }
  
  export interface Road {
    node_id: string
    latitude: number
    longitude: number
    length: number
    name: string
  }
  