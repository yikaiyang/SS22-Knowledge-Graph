export interface TimeResponse {
    response: Response
  }
  
  export interface Response {
    status: string
    data: Data[]
  }
  
  export interface Data {
    node_properties: Time
  }
  
  export interface Time {
    entity_type: string
    node_id: string
    hour: number
    minute: number
    name: string
  }
  