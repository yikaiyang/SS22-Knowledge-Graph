
# Knowledge Graph SS-23 - Knowledge Graph in the Transportation Context

## Motivation
Transportation network optimisation is a challenge that traffic planners / mobility providers are facing. In this area efficiency gains, through better planning, leads to reduced costs and benefits for customers through optimised traffic situations.
The paper “Research on the Construction of a Knowledge Graph and Knowledge Reasoning Model in the Field of Urban Traffic” by Tan et. al. (https://www.mdpi.com/2071-1050/13/6/3191) introduced a solution using a knowledge graph by linking multiple data sources, such as time-dependent passenger trip data, public transport network data. traffic congestion data on streets, road network data and a list of points of interests. Using reasoning models (TransE / TransD) the researchers were able to predict traffic congestion in specific time frames, in relationship to specific point of interests. (e.g. in the paper: schools)

In contrast to the proposal and for time constraint reasons, the construction of the public transit network graph was left out. Since it's only purpose in the paper was to demonstrate the use-case of finding the shortest path between two stations using a Cypher query, it also wouldn't have added a lot of value to the reasoning part of this project.

## Method
The project is divided into 6 sub-parts where the final KG is constructed incrementally. The implementation code can be found in their according subfolders in the submission package

1. <b> Data acquisition:</b> </br>
This project contains code to fetch the data from various data sources providing Road Traffic, Road Incident, Weather, POI (Points of Interest) data.
2. <b> Data processing:</b> </br>
In this project the data acquired from the previous step is processed to extract and transform the values to prepare for the integration to the KG. 
3. <b> Data integration: </b> </br>
This project handles the integration of the processed data into the Neo4J database.
4. <b> KGE - Knowledge Graph Embeddings </b> </br>
In this project various Knowledge Graph Embeddings are trained and evaluated based on the constructed dataset.
5. <b>Application - Web UI and backend service:</b> </br>
This project creates a prototypical Web UI to demonstrate how a KG could serve an potential user, or specialist in the domain of traffic planner.
6. <b>Learning Goals:</b> </br>
To fulfill the learning goals of this lecture, various components that does not fit in the other projects otherwise are implemented here.
7. <b>Conclusion:</b> </br>
In this chapter of this report a conclusion is drawn and the findings of the project are summarized.


## 1. Data acquisition
For this task, data from four different data resources, 
1. Road traffic data (aka. Road congestion data)
2. Road incidents data
3. Weather data
4. Points of interests

were acquired, processed and then integrated into a single ontology:

### 1.1 Road traffic data
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

### Points of interests
Using the Foursquare API, a list of the top 50 most relevant locations of each of the following POI categories were fetched:

<ul>
    <li>Primary School</li>
    <li>Secondary School</li>
    <li>High School</li>
    <li>Middle School</li>
    <li>Private School</li>
    <li>Amusement Park</li>
    <li>Transportation service</li>
    <li>Bus station</li>
    <li>Train station</li>
    <li>Metro Station</li>
    <li>Tram Station</li>
    <li>Transportation services</li>
    <li>Public Transporation</li>
</ul>

As reference the API is documented at the following website: https://location.foursquare.com/places/docs/categories 

![Ontology of this project](/documents/map_area/street_collection_points.png)
*Traffic data of all locations colored in blue were collected*



### Road Incident Data
Road incident data (Traffic incidents / Road closures) was also acquired by fetching from the REST API of the service HERE MAPS.  [Here Maps - Road Traffic](https://developer.here.com/documentation/traffic-api/dev_guide/topics/getting-started/send-request.html)


### Collection Timespan
The data was collected over the timespan of 7 days from Fri, May 6th 2022 - 14:00 to Fri, May 13th 2022 - 17:00 using automated queries in a fixed time-interval of 20 minutes. Due to technical difficulties the data collection from the Traffic Incidents API started at a later time on Tue, March 10 16:45. Thus, the traffic incidents dataset is incomplete since it does not cover the full data collection time period of the other data ressources.


### 2. Data processing

Before the data can be added into the Neo4J database, it has to be processed to receive the necessary format. Two steps had to be taken:

1. Data Linking:
The data from multiple sources had to be merged, and connections to entities from the different datasets had to be established. For example the POI dataset did only contain a pair of geocoordinates (longitude, latitude) missing concrete connections to the streets where those are located. To 

2. Data transformation:
The acquired datasets contained many values that may not be necessary or suitable for the KG. Various values had to be removed or transformed to a different format or data-type to accomodate the needs of the KG.


Since the data was fetched from multiple datasources and each individual script was started at different timings, there is a discrepancy in the collected timestamps of each dataset due to the different request time intervals. Since it is required to combine the different datasets into a single Knowledge Graph the timestamps were rounded in full 20 minutes steps (e.g. 13:32 -> 13:40, and 13:28 -> 13:20) using the script```/documents/match_date_column.py```



*Note: Please disable authentication in NEO4J prior by setting: dbms.security.auth_enabled=false in the NEO4J configuration file.*


## 3. Data Integration: Knowledge Graph Construction
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
A road network can be represented as a graph (V,E), where V (vertices) equals road intersection points, and E (edges) equals road segments. In the paper, data from OpenStreetMaps was fetched using the tool [OSM2GMNS](https://osm2gmns.readthedocs.io/en/latest/) and processed to model the road network. In this exercise submission, due to time constraints, it was refrained from extracting the street network data from OpenStreetMaps, which would have taken too much time for data processing. Instead, the street network was approximated by creating an artificial road network by linking nearby streets using the following method: For every street the nearest 25 streets were computed, while only every i*5-th (i < 25) nearest street was then actually connected in the road network. The idea for applying this method is that it counteracts the formation of disconnected clusters, such that only streets that are very close are connected to each other, while streets in farther distances can not be reached. Obviously, constructing an artificial road network like this will not yield an accurate or correct representation of the real street network, and may distort the results of prediction tasks when applied to Knowledge Graph Embeddings.

![Ontology_example_2](/documents/map_area/street_network.jpg)
*Graph visualization of the street network produced by the approximation method*

## 3. Data Integration
For the integration to the Neo4J database a script 'main.py' which can be found in the folder '3_data_integration' was written which invokes the processing of all data in the form of csv files located in the '/data' folder.

It starts with the deletion of the database and proceeds with the creation of all entities and nodes subsequently relationships. The implementation of those individual creation functions can be found in the file 'data_integration.py'.


## 4. Training: Embeddings
(LO1) To train the embedding model the Python library Pykeen (https://pykeen.github.io) was used. 

For training of the dataset, the same KG models were used, as by the authors of the paper: TransE, TransH, TransD. In addition the model RotatE, and ConvE were added to introduce different concepts (Complex plane / CNN) to the evaluation. 

In the following a statistical breakdown of the dataset characteristics is listed:

| Entities | Triplets | Relationships |
| -------- | -------- | ------------- |
| 1906     | 13006    | 8             |


Distribution of entities:

|Entity/Label   |Count   |
|---|---|
|Road   |591   |
|Weather   |189   |
|Temperature   |495   |
|POI   |524   |
|Date   |13   |
|Time   |72   |
|TrafficSituation   |19   |
|Incident   |3   |


## Results

<h3>Head Entity Prediction (Epochs=50)</h3>

|Model   |MR   |hits@10 |hits@3 | hits@1|
|---|---|---|---|---|
|TransE   |775.5418908531899   |0.77%   |0.08%   |0.00%   |
|TransH   |544.1898539584935   |3.61%   |1.61%   |0.61%   |
|TransD   |766.532667179093   |0.77%   |0.08%   |0.00%   |
|**RotatE**   |**419.2271329746349**   |**4.73%**   |**4.38%**   |**2.65%**   |
|ConvE   |812.8355111452729   |1.00%   |0.35%   |0.04%   |
<h3>Tail Entity Prediction</h3>

|Model   |MR   |hits@10 |hits@3 | hits@1|
|---|---|---|---|---|
|TransE   |805.1898539584935   |0.88%   |0.12%   |0.00%   |
|**TransH**   |324.9792467332821   |**56.23%**   |**55.38%**   |**54.00%**   |
|TransD   |552.4934665641814   |5.00%   |1.58%   |0.00%   |
|RotatE   |**215.44542659492697**   |44.08%   |42.54%   |39.32%   |
|ConvE   |343.7129131437356   |46.93%   |37.39%   |30.55%   |

<h3>Head Entity Prediction (Epochs=100)</h3>

|Model   |MR   |hits@10 |hits@3 | hits@1|
|---|---|---|---|---|
|TransD   |21.313604919292853   |73.60%   |50.31%   |34.70%   |
|TransE   |81.85126825518832   |62.72%   |57.26%   |41.58%   |
|TransH   |**9.021906225980015**   |76.48%   |63.30%   |45.93%   |
|**RotatE**   |13.947732513451191  |**76.98%**   |**65.76%**   |**53.73%**   |
|ConvE   |168.35165257494236   |34.97%   |22.75%   |16.22%   |
<h3>Tail Entity Prediction</h3>

|Model   |MR   |hits@10 |hits@3 | hits@1|
|---|---|---|---|---|
|TransD   |20.55380476556495   |73.64%   |62.53%   |44.04%   |
|TransE   |73.92736356648732   |63.57%   |59.34%   |54.15%   |
|TransH   |**9.028823981552652**   |76.75%   |65.22%   |59.99%   |
|**RotatE**   |10.744427363566487   |**79.05%**   |**67.52%**   |**62.26%**   |
|ConvE   |79.61337432744043   |62.49%   |59.07%   |52.46%   |


## Interpretation
(LO1) In contrast to the findings in the paper by Tan et. al. where the model TransD performed the best, the model TransH performs the best in both Head and Tail-Entity prediction with substantially better results than the other models in all metrics. The reason for this observation could be found in a large number of 1-to-N relationships between the entity 'DateTime' and other entities, since almost every entity except for the type POI is connected to a 'DateTime'. All models seem to perform the best when trained with the number of epochs set to 500-1000 with the performance degrading.  TransH, in contrast to other models uses a hyperplane to model the relationship and hence is able to encode 1-to-N relationships between entities. In theory, the CNN-based ConvE should also do well on n-ary relationships similar to TransH, however during the evaluation seemingly does not yield significantly better results than the other models. Without having a thorough inspection it may be likely that few of the hyperparameters may not be suitable for this project, for example the convolutional mask could be too large / or small and hence causes wrong classifications. What becomes clear though is that the head entity prediction performance using ConvE is severely lacking with a meager accuracy of around 0-6% in all hits@10, hits@3, hits@1 metrics. However this is expected since the underlying Convolutional Neural Network in ConvE works only in one direction.   



At the first glance, the velocity of cars seems to be very slow with no street points measuring speeds above 18km/h. However, this is likely due to the mapping service sampling the velocities and thus returning the average velocity over a timeframe. 


## Real world use-case evaluation
In this segment, the trained model is evaluated against scenarios that are more situated in the real world. 

## Technical Architecture
The technologies used for this project consist of the following:

* NestJS/Node.js for Data Crawling from REST APIs
* Python/Pandas for transfroming the crawled data into a suitable format
* Neo4J as graph database
* PyKeen for training Knowledge Graph Embedding models
* Web UI using Angular/Django backend

## Open questions:
* How to factor in that streets have differenttraffic volume capacities (e.g. streets with single lanes / multiple lanes)
* How do you know that people are not just passing by ?


## Learning Goals

Representations

(LO1) Understand and apply Knowledge Graph Embeddings

Knowledge Graph Embeddings (KGEs) are a large field of representations and techniques focused on a shared principle: how to represent of symbolic knowledge - as in typical databases or datasets (in our case, graphs) - in a sub-symbolic way - as in typical machine learning or deep learning scenarios (in our case, as vectors). We will cover the principles as well as selected seminal and recent KGE models such as the translation-based TransE, the semantic matching-based ComplEx, and the neural network-based ConvE.

In this project

(LO2) Understand and apply logical knowledge

Logical knowledge representation is a broad traditional field of AI techniques rooted across many communities, including of course the knowledge representation and reasoning, databases, semantic web and other communities. As this aspect is covered in many courses, we will focus on (1) giving a short introduction, (2) show connections between the slightly different frameworks used by different communities and (3) focus on an aspect particularly relevant for Knowledge Graphs: how to represent logical knowledge that uses (i) full recursion - as needed by graph processing - and (ii) powerful object creation (existential quantification in logic terms) – as needed to discover unknown parts of a Knowledge Graph.

As the designed system uses a Neo4J database logical queries can be implemented using Cypher queries. As an example a user can look up the shortest path . Another interesting use case would be to look up which streets are commonly exceeding speed limits.

(LO3) Understand and apply Graph Neural Networks

Graph Neural Networks (GNNs) are a rapidly-growing field - successfully applied in many applications – based on a very clear idea: can the structure of the graph (i.e., the symbolic world) be used as the structure of an artificial neural network (ANN) as in typical machine learning and deep learning scenarios. We will cover the principles as well as selected models. The goal is to understand how machine learning and deep learning models based on neural networks can be guided by graph data and knowledge.

(LO4) Compare different Knowledge Graph data models from the database, semantic web, machine learning and data science communities.

KGEs, logical models and GNNs are ways of representing different forms of knowledge in a Knowledge Graph, and thus naturally need to talk about different data models that they are based on. In this part, we will dig deeper into different concrete data models of representing graphs and Knowledge Graphs. One particular focus will be temporal models for Knowledge Graphs. We will give brief overviews of data models from the database, Semantic Web and other communities, and will give pointers to courses that give more details on each of them.
Systems

(LO5) Design and implement architectures of a Knowledge Graph

Designing an IT architecture for any complex AI applications is a challenge, typically requiring to integrate a number of technologies. In this part, we will consider different technology stacks available for Knowledge Graphs, and how to decide which capabilities should be handled by which parts of the architecture. This includes topics such as storing large Knowledge Graphs, and the border between what the Knowledge Graph should handle and what external application code should handle. As a main example, we are going to use the Vadalog system and architecture developed at the University of Oxford together with TU Wien, the Central Bank of Italy and many others. For technology stacks covered in detail by other courses, we will stay high level here and give pointers.

(LO6) Describe and apply scalable reasoning methods in Knowledge Graphs

While storing Knowledge Graphs is an important endeavour in itself, using it to derive new data, insights or other output, is a central service offered by a Knowledge Graph. Typically, for simple questions this is called querying, and for more complex questions and if it requires background knowledge, reasoning. Reasoning is a broad area, and in this part, we will focus on the representations and models most important for Knowledge Graphs: reasoning with KG Embeddings, logical knowledge that allows both full recursion as well as object creation, as well as Graph Neural Networks. We will also consider what it means to reason by combining these aspects.

In terms of the KG embedding component, since most KG embeddings are not transferable and to my knowledge do not support incremental learning, scalability likely poses a big challenge when using a non-static KG which evolves over time, such as in this submission project a KG capturing traffic data. However there is research under way and the paper "Lifelong Embedding Learning and Transfer for Growing Knowledge Graphs" by Cui et. al. introduces the "LKGE" embedding model which takes existing embeddings and fits them to new KG data by using an autoencoder. For now being, the optimal solution is likely to train KGE using snapshots of the KG at specific times, and update the model in a periodical time-frame or when necessary. 

With the current KG schema design the modelling of time poses a great issue in terms of scalability, since for each unit of time a new node / entitiy, in addition to it's relationships to other entities, has to be introduced to the graph. This will result in the KG being bloated with nodes containing time units, likely taking the majority of all entities / relationships in the graph database. A more efficient way to store time would be to introduce concepts like time-trees where not the entire datetime timestamp is stored as a single node, but is split into multiple nodes for each day, month, year, hour and minute unit, and a time representation is then assembled by connecting those units of time.


(LO7) Apply a system to create a Knowledge Graph

In this part, we are going to look at the first part of the Knowledge Graph lifecycle, namely creation. We will give a broad overview of available techniques with some pointers for further information. For Knowledge Graphs this topic includes schema mapping – with many classical techniques stemming from the database community on data exchange and integration, and record linkage, which typically includes an ensemble of Machine Learning methods. These topics will be covered as far as needed for giving a full picture of the KG lifecycle, and connections to other courses will be highlighted.

(LO8) Apply a system to evolve a Knowledge Graph

Evolving a Knowledge Graph is a broad topic, and we are going to cover a representative selection of techniques here. In general, it can be divided into two areas: (i) Knowledge Graph completion (i.e., adding to it). We will here discuss link prediction as a central method, in particular including KG Embeddings as well as logic based reasoning with full recursion and existential quantification. We are also going to discuss how to add knowledge to a KG through techniques such as rule learning or model induction. (ii) Knowledge Graph cleaning (i.e. removing parts of a KG) which can either effect the data or knowledge stored in a KG. This is of course broader, and can include topics such as schema evolution, view maintenance, etc. We will provide a broad picture and pointers for further topics covered in other courses.
Applications

(LO9) Describe and design real-world applications of Knowledge Graphs

Systems and representations are central to this course, but hardly motivated without applications. We will give a broad coverage of real-world applications in many sectors, including: the finance sector, energy sector, logistics and supply chain sector, manufacturing sector, aerospace sector and many others. Our goal is to explore the actual real-world applications of Knowledge Graphs, and learn from them which parts of the broad field of KG techniques are used where, and how to use this for designing such data science and computer science applications ourselves.

In this submission a custom road network knowledge graph was created. The aim of this project was to enable traffic planners or other specialists to see or explore relationships between certain POIs (Points of Interests), street points and road traffic data points. For that data from various datasources were acquired: 1. Foursquare API for POIs, 2. OpenWeatherMap for weather data (temperature / weather condition), 3. HERE Maps API for modelling the road network, as well as road incidents (car accidents / road blocks), and car traffic volume in the form of the average traffic speed. 


(LO11) Apply a system to provide services through a Knowledge Graph

As a final step of creating and then involving a KG, we here give a glimpse into the finale step, namely services that can be provided through Knowledge Graphs. This will necessarily be just an overview, as many AI-based services today use one or more Knowledge Graphs. The typical services that information systems in general provide are in terms of general-purpose or broad analytics provided to a user, or in terms of specific queries or questions asked to a system. While we are point to a specific courses here for more details, we will give a broad overview of how to build structured query interfaces for KG queries and analytics, visualize Knowledge Graphs, build natural language query interfaces for complex KG queries and questions, and build KG-based recommender systems that use deep logic and KGE-based knowledge. In all of these, we will focus on the KG aspects, seeing how in particular a KG is used to support these services. Our goal is here not to understand visualization, recommender systems, etc. – there are specific courses for that – but to understand how an architecture that includes KGs works, and how KGs specifically help these services.

(LO12) Describe the connections between Knowledge Graphs (KGs), Machine Learning (ML) and Artificial Intelligence (AI)

It is clear that Knowledge Graphs are an area of Artificial Intelligence where a number of techniques come together, and where new Machine Learning techniques such as KG Embeddings native to KGs have emergence. Arguably, it is one of the strengths of KG-based systems to allow all such techniques to come together in a well-organized architecture (some call it a “melting pot”). Yet, is all of KGs Artificial Intelligence? What about database systems and highly-scalable data processing techniques? A particularly interesting angle here are the reasoning techniques: How are traditional logic-based reasoning techniques coming together with Machine Learning-based ones? What is the connection to Neural Network-based methods, in particular those where the KG plays a central role (such as in GNNs)? These are questions we will openly consider in this part to allow everyone to not only understand the individual techniques, but how they connect to each other in KGs.

(LO12) Modern KG systems consist of multiple components which have their origins in other areas of computer science, such as database systems, AI, etc. However, while there are certainly overlaps to other areas these are not completely identical since KG systems have specific demands. For example to store the data in a KG, database systems must be used. Traditionally, KG systems do rely on graph-based database systems in contrast to relational, or document-based systems which are more commonly used in traditional software engineering. Those graph-based systems are often tailored to accomodate the needs of a KG, such as more convenient relational queries, the option to store semantic meaning (RDF), even with features such as in-built reasoners in for example GraphDB by Ontotext. Similarly can be said about AI, where techniques from there are used in combination with KGs, such as Neural Networks. Techniques such as embeddings allowed the creation of KG-Embeddings which is itself a novel area and specifically tailored to be used in KGs. Traditional logic-based reasoners  derive information based on existing facts and relationships stored in the KG by using fixed rule-sets (e.g. first-order logic), while machine learning approaches are often using probabilistic methods. Hence, logic-based reasoner are better to derive information when logical consistency / correctness is required, however is lacking in areas when new information has to be derived from the KG which may not be explicitly modelled in the KG, besides from other different characteristics such as in runtime behaviour or the requirement for computation time for training machine learning models. Both techniques can be combined however, for example logic-based reasoners could be used to pre-filter data from the KG to reduce the input and hence the training size for machine-learning based reasoners. Or a logic-based filtering can be applied to the predictions of ML-reasoners afterwards to retrieve logically correct results. Graph Neural Networks in contrast uses information from the neighbourhood to gain understanding about link or node predictions. Hence, it may be more suitable for more tasks which involves the notion of spatiality.  which is inductive in contrast to KG-Embeddings and thus can be applied on . 

Outside of AI, KG systems certainly do also have points of contact with other various areas in Computer Science as well such as in for example in Distributed Computing, or Business Intelligence where specialized techniques such as Stream Processing, Data Warehousing, Horizontal Scaling Techniques can be used to facilitate in preprocessing, maintainance and operation of KGs
Each technology comes with it's own advantages and disadvantages, and their own set of ideal use-cases. For example as was showcased in this project, KG embeddings seem to not really work well on link prediction when used for forecasting the traffic volume in a time-dependent setting. For that traditional GNN, or CNN-based models are likely better suited for those tasks.
In short, KG systems are not entirely made up from AI, however since there are currently many innovations happening in AI which enable many novel techniques and hence use-cases, such as KG-Embeddings, it may seem that KGs are made entirely up of AI. 

From what could be observed is that there is not a single system that trumps others. Implementing a route planning system 