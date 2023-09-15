export interface RelatedNodeResponse {
    response: Response
  }
  
  export interface Response {
    status: string
    data: Data[]
  }
  
  export interface Data {
    node_properties: Location
  }
  
  export interface Location {
    node_id: string
    latitude: number
    longitude: number
    length: number
    name: string
  }
  