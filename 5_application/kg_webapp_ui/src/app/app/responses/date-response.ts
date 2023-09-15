export interface DateResponse {
  response: Response
}

export interface Response {
  status: string
  data: Data[]
}

export interface Data {
  node_properties: Date
}

export interface Date {
  entity_type: string
  node_id: string
  day: number
  month: number
  year: number
  name: string
}
