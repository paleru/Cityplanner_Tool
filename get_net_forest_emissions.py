import json
import requests
import pandas as pd

### should only need to run once, then use csv file to limit network requests ###

sweden = 'SWE'
finland = 'FIN'
aaland = 'ALA'

# assign region_name and region id as k/v pair in dict 
def get_regions(country):
    regions_url = f'https://wri-01.carto.com/api/v2/sql?q=SELECT%20gid_1%20as%20id,%20name_1%20as%20name%20FROM%20gadm36_adm1%20WHERE%20iso%20=%20%27{country}%27%20ORDER%20BY%20name'
    response = requests.get(regions_url)

    data = response.json()
    regions_dict = {row['id'].split('.')[1].split('_')[0]: row['name'] for row in data['rows']}

    return regions_dict

# get every city from each region
def get_cities(country, region_id):
    region_url = f'https://wri-01.carto.com/api/v2/sql?q=SELECT%20gid_2%20as%20id,%20name_2%20as%20name%20FROM%20gadm36_adm2%20WHERE%20iso%20=%20%27{country}%27%20AND%20gid_1%20=%20%27{country}.{region_id}_1%27%20AND%20type_2%20NOT%20IN%20(%27Waterbody%27,%20%27Water%20body%27,%20%27Water%20Body%27)%20ORDER%20BY%20name'
    response = requests.get(region_url)
    return response.json()['rows']

# get net forest emissions for each city
def get_forest_emissions(country, region_id, city_id):
    emissions_url = f'https://www.globalforestwatch.org/api/data/dataset/gadm__tcl__adm2_summary/v20240404/query/?sql=SELECT%20SUM(%22gfw_net_flux_co2e__Mg%22)%20AS%20%22gfw_net_flux_co2e__Mg%22%2C%20SUM(%22gfw_gross_cumulative_aboveground_belowground_co2_removals__Mg%22)%20AS%20%22gfw_gross_cumulative_aboveground_belowground_co2_removals__Mg%22%2C%20SUM(%22gfw_gross_emissions_co2e_all_gases__Mg%22)%20AS%20%22gfw_gross_emissions_co2e_all_gases__Mg%22%2C%20TRUE%20AS%20%22includes_gain_pixels%22%20FROM%20data%20WHERE%20iso%20%3D%20%27{country}%27%20AND%20adm1%20%3D%20{region_id}%20AND%20adm2%20%3D%20{city_id}%20AND%20umd_tree_cover_density_2000__threshold%20%3D%2030'
    response = requests.get(emissions_url)
    data = response.json()
    if data['data']:
        return data['data'][0]['gfw_net_flux_co2e__Mg']
    return None

# create dataframe with region_id, city_id, region_name, city_name, and net_forest_emissions
def create_cities_dataframe(country):
    regions = get_regions(country)
    data = []

    for region_id, region_name in regions.items():
        cities = get_cities(country, region_id)
        for city in cities:
            city_id = city['id'].split('.')[2].split('_')[0]
            net_forest_emissions = get_forest_emissions(country, region_id, city_id)
            data.append({
                'region_id': region_id,
                'city_id': city_id,
                'region_name': region_name,
                'city_name': city['name'],
                'net_forest_emissions_01_to_23': net_forest_emissions
            })

    df = pd.DataFrame(data)
    return df


def create_csv(country):
    cities_df = create_cities_dataframe(country)
    cities_df.to_csv(f'data/net_emissions/{country}_cities.csv', index=False)


def store_in_csv():
    create_csv(sweden)
    create_csv(finland)


#store_in_csv()