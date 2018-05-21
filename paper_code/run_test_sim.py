from InputGeography import InputGeography
from flee.flee import Ecosystem
import os

# plotting imports
import matplotlib as mpl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from analyze_graph import print_graph, print_graph_nx

from scipy.optimize import basinhopping
from scipy.optimize import brute, fmin



def go(args):

	'''	args_vals should be 
	[my_camp_weight, my_conflict_weight, 
					my_min_move, my_max_move,
					my_conflict_move_chance,
					my_camp_move_chance,
					my_default_move_chance]'''

	pd.DataFrame(args).T.to_csv('flee/my_settings.csv', 
		header = False, index = False, sep = "|")


	geog = InputGeography()
	geog.ReadLocationsFromCSV(FILES["locations_init"])


	geog.ReadLinksFromCSV(csv_name = FILES["routes"])

	e = Ecosystem()

	e, lm = geog.StoreInputGeographyInEcosystem(e)
	
	# use lm object to look up starting place for each agent

	lm_key = list(lm.keys())

	res_list = {}
	for i in lm_key:
		if i not in res_list:
			res_list[i] = []
	err_list = {}
	for i in lm_key:
		if i not in err_list:
			err_list[i] = []

	conflict_locations = pd.read_csv(FILES["conflict_locs"])
	num_rounds = len(set(conflict_locations['round']))

	for each_step in range(num_rounds):

		candidate_zone = conflict_locations[conflict_locations['round'] == each_step]
		new_conflicts = set(candidate_zone.name)
		for i in new_conflicts:
			if i not in e.conflict_zone_names:
				e.add_conflict_zone(i)
		peace_transition = [i for i in lm_key if i not in new_conflicts ]
		for i in peace_transition:
			e.remove_conflict_zone(i)


		num_tot = {}


		for each_agent in range(0, 100):
			place = np.random.randint(0, len(lm_key))
			e.addAgent(location=lm[lm_key[place]])

		e.refresh_conflict_weights()

		e.evolve()

		loc_list = []
		for each_location, loc_obj in lm.items():
			#try:
			res_list[each_location].append(loc_obj.numAgents)


	results_df = pd.DataFrame(res_list)
	results_df.to_csv('results_of_sim.csv')
	results_val = [int(i) for i in results_df.iloc[-1,:]]
	results_denom = sum(results_val)
	results_columns = list(results_df.columns)

	truth_df = pd.read_csv(FILES['truth_values'], skiprows =1, header = None)
	truth_val = [int(i) for i in truth_df.iloc[-1, :]]
	truth_denom = sum(truth_val)
	truth_columns = list(truth_df.iloc[0, :])

	truth_dict = dict(zip(truth_columns, [i/truth_denom for i in truth_val]))
	result_dict = dict(zip(results_columns, [i/results_denom for i in results_val]))
	error_list = []
	error_places = []

	for result_key, result_item in result_dict.items():
		#print(result_key, "AGSINST", truth_dict)
		if result_key in truth_dict:
			error = abs(truth_dict[result_key] - result_item)
			print("for {}, error is {}".format(result_key, error))
			error_list.append(error)
			error_places.append(result_key)
		else:
			pass
			#error = result_item
	pd.DataFrame([error_places, error_list]).T.to_csv('errors_results.csv')
	return np.mean(error_list)



if __name__ == "__main__":

	'''	args_vals = [my_camp_weight, my_conflict_weight, 
					my_min_move, my_max_move,
					my_conflict_move_chance,
					my_camp_move_chance,
					my_default_move_chance]'''

	FILES = {"locations": 'data/settled_locations/irq_pplp_ocha_20140722.shp',
				"routes": 'data/routes_admin1_centroids.csv',
				"start_state_pops": 'iom_dtm_reports/d84.csv',
				"locations_init": "data/location_values_init2.csv",
				"conflict_data": 'data/acled_unprocessed_conflict_locations.csv',
				"conflict_locs": 'data/conflict_locations_by_round2.csv',
				"end_state_pops": 'iom_dtm_reports/r91.csv',
				"truth_values": 'truth_vals.csv',
				}

	minimizer_kwargs = {"method": "BFGS"}

	x0 = [5, 0.2, 10, 10, 0.1, 0.1, 0.1]

	ret = basinhopping(go, x0, 
		minimizer_kwargs=minimizer_kwargs,
		niter=2)

	#rranges = (slice(0,1,0.1), slice(0, 1, 0.1),
		       #slice(0, 100, 10), slice(0, 1000, 100),
		       #slice(0, 1.0, 0.1), slice(0, 1.0, 0.1),
		       #slice(0, 1.0, 0.1))
	#ret = brute(go, rranges, disp = True)#,
					#finish = fmin)

	#ret = go([2, 0.5, 1, 1000, 0.1, 0.9, 0.8])
	print(ret)
	#go_vals = [ 4.26642083e+00, -7.02500877e-03,  1.01585004e+01,  1.05621909e+01, -9.07899883e-02, -2.07080421e-01, -6.62580836e-01]
	#go_vals = [ 5.17107326, -0.39410599,  9.92363267, 10.17238293, -0.81284913,
        #0.67581873,  0.37396598]

	#print("BEST PARAMS", ret[0])
	#print("PROVIDE ERROR OF", go(go_vals))

	#print("global minimum: x = %.4f, f(x0) = %.4f" % (ret.x, ret.fun))

