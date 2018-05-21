

# This is data cleaning and preparation code

import geopandas as gpd
import pandas as pd 
from shapely.geometry import Point
import matplotlib.pyplot as plt 


class DataSets:


	def __init__(self):
		self.locations = None
		self.districts = None
		self.locations_dissolved = None
		self.routes = None
		self.starting_pops = None
		self.locs_w_pop = None


	def clean_data(self, files):
		'''Clean data by running successive functions. 
		'''
		self.get_locations(files['locations'])
		self.dissolve_locations()
		self.calc_distances(files['routes'])
		self.find_observed_pop_init(files)
		self.get_conflict_locations(files)
		self.find_observed_pop_final(files)


	def get_locations(self, file_loc):
		self.locations = gpd.read_file(file_loc)

	def dissolve_locations(self):
		self.locations_dissolved = self.locations.copy().dissolve(by='A1NameEn')

	def calc_distances(self, out_file):
		'''Calculate all distances between locations
		'''
		tmp_loc = self.locations_dissolved.copy().reset_index()
		tmp_loc['geometry'] = tmp_loc['geometry'].centroid
		trips = set()
		count = 0
		routes = []
		for i in tmp_loc.itertuples():
			dists = tmp_loc.geometry.distance(i.geometry)  * 1000
			dists = [int(round(i,0)) for i in dists]
			tups = zip(tmp_loc.A1NameEn, dists)
			for destination, time in tups:
				key = (i.A1NameEn, destination)
				if key[0] == key[1]:
					continue
				else:
					trips.add(key)
					trips.add((key[1], key[0]))
					routes.append([key[0], key[1], time])
					if key[0] != key[1]:
						routes.append([key[1], key[0], time])
		self.routes = pd.DataFrame(routes)
		self.routes.columns = ["start", "end", "dist"]
		self.routes.to_csv(out_file)

	def find_observed_pop_init(self, files):
		'''Find the starting point population
		'''
		tmp_loc = self.locations_dissolved.copy()
		tmp_loc['geometry'] = tmp_loc.geometry.convex_hull

		pops = pd.read_csv(files['start_state_pops'], 
							usecols  = ['Latitude', 'Longitude', 'Families', 
										'Individuals', 'District'])
		pops = gpd.GeoDataFrame(pops)
		pops.crs = tmp_loc.crs
		pops['geometry'] = [Point(x,y) for x, y in zip(pops.Longitude, pops.Latitude)]
		


		pops = pops[['District', 'geometry', 'Families', 'Individuals']]
		pops = pops.dissolve(by = 'District', aggfunc = 'sum')
		pops['geometry'] = pops.geometry.centroid

		locs_w_pop = gpd.sjoin(tmp_loc, pops).reset_index()
		locs_w_pop = locs_w_pop.dissolve('index', aggfunc = 'sum')
		locs_w_pop = locs_w_pop.reset_index()

		self.locs_w_pop = locs_w_pop

		self.starting_pops = pd.DataFrame()
		geoms = self.locs_w_pop.geometry.centroid
		self.starting_pops['name'] = locs_w_pop['index']
		self.starting_pops['lat'] = [i.y for i in geoms]
		self.starting_pops['lon'] = [i.x for i in geoms]
		self.starting_pops['pop'] = locs_w_pop['Families']

		self.starting_pops.to_csv(files['locations_init'])

	def find_observed_pop_final(self, files):
		''' Find the end-state population
		'''
		tmp_loc = self.locations_dissolved.copy()
		tmp_loc['geometry'] = tmp_loc.geometry.convex_hull
		
		pops = pd.read_csv(files['end_state_pops'], usecols = ['Latitude', 
												'Longitude', 'Families',
												 'Individuals', 'Governorate'])
		pops = gpd.GeoDataFrame(pops)
		pops['geometry'] = [Point(x,y) for x, y in zip(pops.Longitude, pops.Latitude)]
		pops = pops.dissolve(by = 'Governorate', aggfunc='sum')
		pops['geometry'] = pops.geometry.centroid

		locs_w_pop = gpd.sjoin(tmp_loc, pops).reset_index()
		locs_w_pop = locs_w_pop.dissolve('index', aggfunc = 'sum')
		locs_w_pop = locs_w_pop.reset_index()

		location_csv = pd.DataFrame()
		location_csv['name'] = locs_w_pop['index']
		location_csv['pop'] = locs_w_pop['Families']
		location_csv.fillna(0, inplace = True)
		location_csv.T.to_csv(files['truth_values'], header = True, index = False)


	def get_conflict_locations(self, files):
		'''Find the places which are conflict locations and at which step
		'''

		conflict_loc = pd.read_csv(files['conflict_data'])
		conflict_loc = conflict_loc[conflict_loc['fatalities'] > 0]
		conflict_loc = gpd.GeoDataFrame(conflict_loc)
		points = [Point(float(j), float(i)) for i, j in zip(conflict_loc.latitude, conflict_loc.longitude)]
		conflict_loc.geometry = points
		conflict_loc = conflict_loc.sort_values('event_date')

		new_x = lambda x: int(x[:4] + x[5:7] + x[8:])
		date_int = [new_x(i) for i in conflict_loc['event_date']]

		conflict_loc['event_date_int'] = date_int
		conflict_loc = conflict_loc[conflict_loc['event_date_int'] > 20171129]

		conflict_loc['round'] =  conflict_loc.event_date_int.apply(assign_round)

		locs = gpd.sjoin(self.locs_w_pop, conflict_loc).reset_index()

		locs = locs[['index', 'round']]
		locs.columns =['name', 'round']

		locs.to_csv(files['conflict_locs'])



def assign_round(new_x):
    '''Helper to assign rounds correctly
    '''
    start = 20170101
    # from http://iraqdtm.iom.int/IDPsML.aspx
    upper_dates = [20170105, 20170119, 20170202, 20170216, 
                  20170302, 20170316, 20170330, 20170413, 
                  20170427, 20170515, 20170530, 20170615,
                  20170630, 20170715, 20170730, 20170815,
                  20170830, 20170915, 20170930, 20171015, 
                  20171031, 20171115, 20171129, 20171215,
                  20171231,
                  20180115,20180131, 20180215, 20180228, 
                  20180315, 20180330, 20180415, 20180430,
                  ]
    top_val = len(upper_dates)
    offset = len(upper_dates)
    
    for i in upper_dates:
        if new_x > i:
            offset -= 1
            start = i
        else:
            return top_val - offset


if __name__ == "__main__":

	# list all files used here in this dict. 

	files = {"locations": 'data/settled_locations/irq_pplp_ocha_20140722.shp',
				"routes": 'data/routes_admin1_centroids.csv',
				"start_state_pops": 'iom_dtm_reports/d84.csv',
				"locations_init": "data/location_values_init2.csv",
				"conflict_data": 'data/acled_unprocessed_conflict_locations.csv',
				"conflict_locs": 'data/conflict_locations_by_round2.csv',
				"end_state_pops": 'iom_dtm_reports/r91.csv',
				"truth_values": 'truth_vals.csv',
				}

	d = DataSets()
	d.clean_data(files)



