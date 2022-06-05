// Create entities
CREATE (r:Road)
CREATE (p:POI)
CREATE (p:POICategory)
CREATE (d:Date)
CREATE (t:Time)
CREATE (ts:TrafficSituation)
CREATE (w:Weather)
CREATE (i:Incident)

// Create relationships
(d:Date)<-[:ROAD_DATE]-(r:Road)
(t:Time)<-[:DATE_TIME]-(d:Date)
(ts:TrafficSituation)<-[:HAVE]-(t:Time)
(p:POI)-[:IS]->(c:category)
(t:Time)-[:HAS_WEATHER]->(w:weather)
(r:Road)<-[:IS_LOCATED]-(p:POI)
(r:Road)-[:HAS_INCIDENT]->(i:Incident)


// (:Road {
//     name: string,
//     latitude: number,
//     longitude: number,
//     length: number,
// })<-[:IS_NEARBY]-
// (:POI {
//     name: string, 
//     latitude: number,
//     longitude: number,
//     category: string
// })
