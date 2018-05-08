from InputGeography import InputGeography
from flee.flee import Ecosystem
import os

# plotting imports
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from analyze_graph import print_graph, print_graph_nx


def go():
	geog = InputGeography()
	geog.ReadLocationsFromCSV('data/location_values_init.csv',							
							name_col = 0,
							population_col = 3 ,
							gps_x_col = 2,
							gps_y_col = 1)


	geog.ReadLinksFromCSV(csv_name = 'data/routes_admin1.csv',
							name1_col = 0,
							name2_col = 1,
							dist_col = 2)
	print("Geography loaded\n")

	e = Ecosystem()
	print("Ecosystem created\n")

	#print("End time is: {}".format(end_time))

	e, lm = geog.StoreInputGeographyInEcosystem(e)
	print("Geography stored in Ecosystem")
	
	# use lm object to look up starting place for each agent

	import numpy as np 
	lm_key = list(lm.keys())

	import pandas as pd
	res_list = {}
	for i in lm_key:
		if i not in res_list:
			res_list[i] = []
	err_list = {}
	for i in lm_key:
		if i not in err_list:
			err_list[i] = []

	import pandas as pd
	conflict_locations = pd.read_csv('data/conflict_locations_by_round.csv')


	for each_step in range(16):

		print("current conflict zones are", e.conflict_zone_names)

		candidate_zone = conflict_locations[conflict_locations['round'] == each_step]
		new_conflicts = set(candidate_zone.name)
		for i in new_conflicts:
			if i not in e.conflict_zone_names:
				e.add_conflict_zone(i)
		peace_transition = [i for i in lm_key if i not in new_conflicts ]
		for i in peace_transition:
			e.remove_conflict_zone(i)
		print("PEACE", peace_transition)
		print("\nCONF:", e.conflict_zone_names)


		num_tot = {}

		e.refresh_conflict_weights()


		for each_agent in range(0, 1000):
			place = np.random.randint(0, len(lm_key))
			e.addAgent(location=lm[lm_key[place]])

		e.evolve()

		e.printInfo()
		print("\n---------")
		print("\nTIME IS: {}".format(each_step))

		loc_list = []
		for each_location, loc_obj in lm.items():
			try:
				res_list[each_location].append(loc_obj.numAgents)
			except:
				pass
		for each_location,loc_obj in lm.items():
			try:
				error = abs(num_tot[each_location] - loc_obj.numAgents)
				err_list[each_location].append(error)
			except:
				pass

	results = pd.DataFrame(res_list)
	print(results.shape)

	#results.columns = lm_key
	truth = pd.read_csv('truth_vals.csv', skiprows =1, header = None)
	errors = []
	for i in range(16):
		truth_val = truth.iloc[:,i]/truth.T.sum()[i]
		result_val = results.iloc[:,i]/results.T.sum()[i]
		errors.append(sum(abs(truth_val - result_val)))

	print(errors)



	# need to compare with some loss function


if __name__ == "__main__":
	go()