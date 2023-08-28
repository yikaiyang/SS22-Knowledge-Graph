export interface IncidentResponse {
    response: Response
}

export interface Response {
    status: string
    data: Data[]
}

export interface Data {
    node_properties: Incident
}

export interface Incident {
    node_id: string
    criticality: string
    incident_type: string
    latitude: number
    longitude: number
    name: string
} 