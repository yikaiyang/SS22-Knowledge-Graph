export interface POIResponse {
  response: Response
}

export interface Response {
  status: string
  data: Data[]
}

export interface Data {
  node_properties: POI
}

export interface POI {
  entity_type?: string
  node_id: string
  latitude: number
  longitude: number
  name: string
  category?: string
}
