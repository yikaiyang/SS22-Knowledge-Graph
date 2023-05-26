from data_transformation.incident_transform import transform_incidents
from data_transformation.traffic_transform import transform_traffic
from data_transformation.weather_transform import transform_weather
from data_transformation import match_date_column
from data_linking import export_roads_list, calc_nearby_roads

if __name__ == "__main__":
    print('Starting script')
    
    # 1) First, data is transformed from raw data
    # transform_incidents()
    # transform_traffic()
    # transform_weather()
    
    # 2) Second, data between datapoints are linked
    #export_roads_list.export_all_roads()
    #calc_nearby_roads.add_nearby_roads_to_roads_file()
    match_date_column.match_date_column()
    
    # 3) Third, data is integrated to the database
    