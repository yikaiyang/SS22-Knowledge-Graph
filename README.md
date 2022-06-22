
# Knowledge Graph SS-22 - Knowledge Graph in the Transportation Context

## Motivation
Transportation network optimisation is a challenge that traffic planners / mobility providers are facing. In this area efficiency gains, through better planning, leads to reduced costs and benefits for customers through optimised traffic situations.
The paper “Research on the Construction of a Knowledge Graph and Knowledge Reasoning Model in the Field of Urban Traffic” by Tan et. al. (https://www.mdpi.com/2071-1050/13/6/3191) introduced a solution using a knowledge graph by linking multiple data sources, such as time-dependent passenger trip data, public transport network data. traffic congestion data on streets, road network data and a list of points of interests. Using reasoning models (TransE / TransD) the researchers were able to predict traffic congestion in specific time frames, in relationship to specific point of interests. (e.g. in the paper: schools)

In contrast to the proposal and for time constraint reasons, the construction of the public transit network graph was left out. Since it's only purpose was to demonstrate the use-case of "finding the shortest path between two stations" using a Cypher query, it also wouldn't have added a lot of value to the exercise in the context of this class, which is more focused on the reasoning side.

## Method


## 1. Data acquisition
For this task, data from four different data resources, 
1. Road traffic data (aka. Road congestion data)
2. Road incidents data
3. Weather data
4. Points of interests

were acquired, processed and then integrated into a single ontology:

### Road traffic data
Road traffic data was acquired from the online mapping application HERE MAPS, which provides a publicly available REST-API to query realtime traffic data. [Here Maps - Road Traffic](https://developer.here.com/documentation/traffic-api/dev_guide/topics/getting-started/send-request.html)

The following examplary HTTP Request shows a query to retrieve the traffic data nearby a location (latitude, longitude) within a radius of 2000m.
```
https://data.traffic.hereapi.com/v7/flow?in=circle:48.189101,16.338981;r=2000&locationReferencing=olr
```
Similarly to the paper by Tan et. al. the observed area was restricted to a specific corridor in order to reduce the scope of the modeled road network. A road with high traffic fluctuation during different daytime hours was then selected. (in the Paper: Fifth Ring Road of Beijing, in this exercise: Gürtelstrasse / Donaukanal of the City of Vienna) 

Using the website "geojson.io" [GeoJSON](https://geojson.io/#map=2/20.0/0.0) a path was manually drawn that resembles the outline of the outer "ring" road of the city of Vienna and it's path extracted as a file in the GEOJSON format. To ensure compatibility with the Here Maps REST API the encoded pathway is then converted into the Flexible-Polyline encoding. [Flex-Polyline](https://github.com/heremaps/flexible-polyline)

The pathway shown graphically:
![Selected Road](/documents/map_area/map_area.png)
*Pathway of streets where traffic data collection is envisioned*


<br/>
The pathway encoded in GEOJSON encoding

<details>
  <summary>Click to reveal</summary>
  
```
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        16.3559,
                        48.23279
                    ],
                    [
                        16.36036,
                        48.233360000000005
                    ],
                    [
                        16.36293,
                        48.228100000000005
                    ],
                    [
                        16.366709999999998,
                        48.224900000000005
                    ],
                    [
                        16.367569999999997,
                        48.22044
                    ],
                    [
                        16.371689999999997,
                        48.21678
                    ],
                    [
                        16.37512,
                        48.21278
                    ],
                    [
                        16.38216,
                        48.21118
                    ],
                    [
                        16.386969999999998,
                        48.21266
                    ],
                    [
                        16.39332,
                        48.21232
                    ],
                    [
                        16.39606,
                        48.20854
                    ],
                    [
                        16.39658,
                        48.20431
                    ],
                    [
                        16.40173,
                        48.201679999999996
                    ],
                    [
                        16.40636,
                        48.200649999999996
                    ],
                    [
                        16.409969999999998,
                        48.19665
                    ],
                    [
                        16.40104,
                        48.19104
                    ],
                    [
                        16.395719999999997,
                        48.18623
                    ],
                    [
                        16.39212,
                        48.18806
                    ],
                    [
                        16.380959999999998,
                        48.18818
                    ],
                    [
                        16.372889999999998,
                        48.18589
                    ],
                    [
                        16.364649999999997,
                        48.18314
                    ],
                    [
                        16.358299999999996,
                        48.180620000000005
                    ],
                    [
                        16.352459999999997,
                        48.17994
                    ],
                    [
                        16.348169999999996,
                        48.18085
                    ],
                    [
                        16.345599999999997,
                        48.18429
                    ],
                    [
                        16.342509999999997,
                        48.18806
                    ],
                    [
                        16.339239999999997,
                        48.18795
                    ],
                    [
                        16.337529999999997,
                        48.19092
                    ],
                    [
                        16.3389,
                        48.19516
                    ],
                    [
                        16.337529999999997,
                        48.20088
                    ],
                    [
                        16.336669999999998,
                        48.20614
                    ],
                    [
                        16.338209999999997,
                        48.20946
                    ],
                    [
                        16.338729999999998,
                        48.21255
                    ],
                    [
                        16.341299999999997,
                        48.21701
                    ],
                    [
                        16.343359999999997,
                        48.22124
                    ],
                    [
                        16.348169999999996,
                        48.223870000000005
                    ],
                    [
                        16.349539999999998,
                        48.22970000000001
                    ],
                    [
                        16.354349999999997,
                        48.232220000000005
                    ],
                    [
                        16.3559,
                        48.23279
                    ],
                    [
                        16.36036,
                        48.233360000000005
                    ],
                    [
                        16.36293,
                        48.228100000000005
                    ],
                    [
                        16.366709999999998,
                        48.224900000000005
                    ],
                    [
                        16.367569999999997,
                        48.22044
                    ],
                    [
                        16.371689999999997,
                        48.21678
                    ],
                    [
                        16.37512,
                        48.21278
                    ],
                    [
                        16.38216,
                        48.21118
                    ],
                    [
                        16.386969999999998,
                        48.21266
                    ],
                    [
                        16.39332,
                        48.21232
                    ],
                    [
                        16.39606,
                        48.20854
                    ],
                    [
                        16.39658,
                        48.20431
                    ],
                    [
                        16.40173,
                        48.201679999999996
                    ],
                    [
                        16.40636,
                        48.200649999999996
                    ],
                    [
                        16.409969999999998,
                        48.19665
                    ],
                    [
                        16.40104,
                        48.19104
                    ],
                    [
                        16.395719999999997,
                        48.18623
                    ],
                    [
                        16.39212,
                        48.18806
                    ],
                    [
                        16.380959999999998,
                        48.18818
                    ],
                    [
                        16.372889999999998,
                        48.18589
                    ],
                    [
                        16.364649999999997,
                        48.18314
                    ],
                    [
                        16.358299999999996,
                        48.180620000000005
                    ],
                    [
                        16.352459999999997,
                        48.17994
                    ],
                    [
                        16.348169999999996,
                        48.18085
                    ],
                    [
                        16.345599999999997,
                        48.18429
                    ],
                    [
                        16.342509999999997,
                        48.18806
                    ],
                    [
                        16.339239999999997,
                        48.18795
                    ],
                    [
                        16.337529999999997,
                        48.19092
                    ],
                    [
                        16.3389,
                        48.19516
                    ],
                    [
                        16.337529999999997,
                        48.20088
                    ],
                    [
                        16.336669999999998,
                        48.20614
                    ],
                    [
                        16.338209999999997,
                        48.20946
                    ],
                    [
                        16.338729999999998,
                        48.21255
                    ],
                    [
                        16.341299999999997,
                        48.21701
                    ],
                    [
                        16.343359999999997,
                        48.22124
                    ],
                    [
                        16.348169999999996,
                        48.223870000000005
                    ],
                    [
                        16.349539999999998,
                        48.22970000000001
                    ],
                    [
                        16.354349999999997,
                        48.232220000000005
                    ]
                ]
            }
        }
    ]
}
```
</details>



The pathway encoded in Flexible-Polyline encoding:
```
BF-usmJsw6jDyD8b7gBiQ_T0X7bsF7W4Z_YuV_JgsBoJiejC2nBzXkRtaoDtQmgBtG-c_YyWhjB53BhenhBuLvWY3lCpOtyBlRvzB3P1nBnEvkB2F5awVhQyXpTVtUyS1KwayI4jBxI8gBrF4U0JqToD8biQua8MuQieukByI4Pie
```

The following request queries the traffic flow information of the viennese outer "ring" road. (Gürtel - Donaukanalstrasse - Gürtel) and all streets in the perimeter of 200 meters:

To access API resource the GEOJSON string has to be converted as FlexPolyPoint string.
```
https://data.traffic.hereapi.com/v7/flow?in=corridor:BF-usmJsw6jDyD8b7gBiQ_T0X7bsF7W4Z_YuV_JgsBoJiejC2nBzXkRtaoDtQmgBtG-c_YyWhjB53BhenhBuLvWY3lCpOtyBlRvzB3P1nBnEvkB2F5awVhQyXpTVtUyS1KwayI4jBxI8gBrF4U0JqToD8biQua8MuQieukByI4Pie;r=200&locationReferencing=shape&apiKey={YOUR_API_KEY}
```

The returning HTTP response contains the data about the traffic situation of all street points (blue dots) at the time of the request depicted in the following figure:

![Ontology of this project](/documents/map_area/street_collection_points.png)
*Traffic data of all street points in blue are collected*



### Road Incident Data
Road incident data can be queried by the service HERE MAPS as well. 


### Collection Timespan
The data was collected over the timespan of 7 days from Fri, May 6th 2022 - 14:00 to Fri, May 13th 2022 - 17:00 using automated queries in a fixed time-interval of 20 minutes. Due to technical difficulties the data collection from the Traffic Incidents API started at a later time on Tue, March 10 16:45. Thus, the traffic incidents dataset is incomplete since it does not cover the full data collection time period of the other data ressources which may introduce a Bias during the training phase of the embedding model. To accommodate this issue, a second batch of data was created by letting the scripts continuing running unti Wed, May 18th 21:00.

### Data processing
Since there is an individual script for querying each REST ressource, and each script were manually invoked, there is a discrepancy in the collected timestamps of each dataset. (e.g. 11:21 in the traffic dataset , while the traffic incident dataset has 11:24, due to the script starting 3 minutes later) However, since it is required to combine the different datasets to enable reasoning over the relationships of the different datasets, the timestamps were rounded to the next timestamp in full 20 minutes steps. (E.g. 13:32 -> 13:40, and 13:28 -> 13:20)

The script ```/documents/match_date_column.py``` adjusts the time value, as aforementioned, for each csv file.

*Note: Please disable authentication in NEO4J prior by setting: dbms.security.auth_enabled=false in the NEO4J configuration file.*


## 2. Knowledge Graph Construction
The structure of the ontology is derived from the ontology presented in the paper by Tan et. al. However, some adjustments were made to incorporate weather and incident data.

![Ontology by Tan et al.](/documents/ontology_graphic/ontology_paper.png)
*Fig.2: Original Ontology by Tan et al.*

![Ontology of this project](/documents/ontology_graphic/ontology.png)
*Modified Ontology used in this exercise submission*

### 2.1. Modelling Time
Due to the time-dependent nature of the data, especially in the transportation domain where the traffic situation is highly dynamic and changes based on the time of observation, time must be modelled or represented in the knowledge graph. The authors applied a method similarly to the Time-Tree model to the Neo4J database by introducing vertices representing the hour and minute values and connecting all entities associated with that time using edges. However, the modelling method used by the study authors raises some concerns.

The construction using this method can be done in the following ways (which one the study authors were using is unclear):

1) Method 1: Creation of date and time vertices only once, so that there are no duplicates of a timestamp in the entire knowledge graph, and create relationships between the entities associated with the timestamp. However, by using this approach, the information of the initial relationship chain between entities is lost, since now all entities associated with a specific time are also in relation to each other.
<br/> <br/>
To illustrate the problem, the following example is given:
Let's suppose that there are two entities of type street: Street 1 and Street 2. Street 1 has a favorable/good traffic situation (green) at 14:00h, while at the same time the traffic situation at Street 2 is bad (red). When added to the ontology, it is now not possible to determine which traffic situation belongs to which exact street. Moreover, every street in the ontology would now stand in relation to all traffic situations, no matter if those traffic situations had actually occured in the respective streets. E.g. Street 1 is now simultaneously associated to the traffic situation entities 'good' and 'bad', even though only the traffic situation 'good' is valid for Street 1.

![Ontology_example_1](/documents/ontology_graphic/concrete_ontology_example_1.png)
*Example of a concrete ontology where invalid relationships are introduced.*

2) Method 2: Creation of individual date and time vertices for every entity associated with a timestamp. This will incur that nodes will be created for each time and hour for each entity associated with that timestamp. The advantage of this approach would be that it is able to preserve correctness between relationships of entities that are linked by time. The issue with this solution is now that each time-associated entity creates their own time entities, hence all time entities are distinct even if they have the same time value (e.g. multiple nodes with the value 14:00). Thus, the loss of semantics of time could play a role on how the predictions of KG embeddings turn out.

![Ontology_example_2](/documents/ontology_graphic/concrete_ontology_example_2.png)
*Example of a concrete ontology where an entity is created for each timestamp. Time entities, which represent the same time are not connected to each other.*

Since time dependent data is quite common in datasets, this area has been already researched and the optimal solution would likely be to use Knowledge Graph Embeddings specialized on temporal facts instead. Such as HyTE, which would be able to preserve temporal consistency. By using this method, the modelling of the ontology would change accordingly, as distinctive entities for representing time are not needed anymore, as seen in the following figure:

![Ontology_example_3](/documents/ontology_graphic/ontology-temporal.png)
*Remodeled ontology with time entities removed by using incorporating time as an attribute in the relationships itself*

Based on those observations and the fact that the relationship between the road entities and time entities is called 'road_date', it may can be implicitly assumed that the study authors have used method 2. Still, due to the large amounts of edges and nodes that would be needed to be created by using method 2, and the incurred higher processing power and hardware needs, it was decided to use method 1 for this exercise.

## Road Network Creation

A road network can be represented as a graph (V,E), where V (vertices) equals road intersection points, and E (edges) equals road segments. In the paper, data from OpenStreetMaps was fetched using the tool [OSM2GMNS](https://osm2gmns.readthedocs.io/en/latest/) and processed to model the road network. In this exercise submission, due to time constraints, it was refrained from extracting the street network data from OpenStreetMaps, which would have entailed additional data processing. Instead, the street network was approximated by creating an artificial road network by linking nearby streets. For every street the nearest 25 streets were computed, while only every i*5-th nearest street (for i < 25) was taken. The background for applying this method is that it counteracts the formation of clusters, such that only streets that are very close are connected while streets in farther distances can not be reached. Obviously, constructing a road network using this method does not yield an accurate or correct representation of the real street network, and will create new and leave out many street connections which exist or do not exist in the real world.
![Ontology_example_2](/documents/map_area/street_network.jpg)
*Graph visualization of the street network produced by the approximation method*

## 3. Training: Embeddings
To train the embedding model the python package pykg2vec from the library PyTorch is used: https://analyticsindiamag.com/pykg2vec/

For training the dataset, it was initially planned to use TransE / TransD embeddings, as used by the authors of the paper.

|Entities   |Triplets   |Relationships |Training Set   |Test Set   |Validation Set   |
|---|---|---|---|---|---|
|33157   |44343   |   |   |   |   |

## Results


## Conclusion


## Technical Architecture
The technologies used for this exercise submission consist of:

* NestJS/Node.js as data crawler
* Python/Pandas for transfroming the crawled data into a suitable format
* Neo4J as graph database
* PyKeen for training embeddings

## Open questions:
* How to factor in that streets have differenttraffic volume capacities (e.g. streets with single lanes / multiple lanes)
* How do you know that people are not just passing by ?