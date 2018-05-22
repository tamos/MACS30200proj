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

from pickle import dumps


class Simulation:

	def __init__(self):
		self.training = Training()
		self.testing = Testing()


class Testing:

	def __init__(self):
		self.results = None

	def test(self, params):
		self.results = go_test(params)
		print(self.results)


class Training:

	def __init__(self):
		self.results = {}

	def basinhopper(self, minimizer_kwargs, x0, **kwargs):

		self.results['basinhopping'] = basinhopping(go, x0, 
			minimizer_kwargs=minimizer_kwargs, seed = 1234,
			**kwargs)
		print("Basinhopper Trained")

	def brute(self, rranges, **kwargs):
		self.results['brute'] = brute(go, rranges, **kwargs)
		print("Brute Trained")



def bad_args(args):
	# make sure min and max are in right order
	if args[2] < args[3]:
		return True
	# make sure probs are not negative
	elif args[4] < 0:
		return True
	elif args[5] < 0:
		return True
	elif args[6] < 0:
		return True
	else:
		return False

def go(args):

	'''	args_vals should be 
	[my_camp_weight, my_conflict_weight, 
					my_min_move, my_max_move,
					my_conflict_move_chance,
					my_camp_move_chance,
					my_default_move_chance]'''

	# first make sure args are valid, return large value if they are
	if bad_args(args):
		return 0.9

	###### SET UP #####

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

	###### TRAINING #####

	for each_step in TRAIN_SET:

		candidate_zone = conflict_locations[conflict_locations['round'] == each_step]
		new_conflicts = set(candidate_zone.name)
		for i in new_conflicts:
			if i not in e.conflict_zone_names:
				e.add_conflict_zone(i)
		peace_transition = [i for i in lm_key if i not in new_conflicts ]
		for i in peace_transition:
			e.remove_conflict_zone(i)

		num_tot = {}

		for each_agent in range(0, 1000):
			place = np.random.randint(0, len(lm_key))
			e.addAgent(location=lm[lm_key[place]])

		e.refresh_conflict_weights()

		e.evolve()

		for each_location, loc_obj in lm.items():
			res_list[each_location].append(loc_obj.numAgents)


	###### CALCULATING ERROR #####

	results_df = pd.DataFrame(res_list)
	results_df.to_csv('raw_results_of_sim.csv')

	# Get the validation values
	truth_df = pd.read_csv(FILES['valid_values'], skiprows =1, header = None)

	# Get the number of observed families
	truth_val = [int(i) for i in truth_df.iloc[-1, :]]

	# Get the total number of observed families
	truth_denom = sum(truth_val)

	# Get the locations of the families
	truth_columns = list(truth_df.iloc[0, :])

	# account for missing counts in truth 

	results_keep = [i for i in results_df.columns if i in truth_columns]

	results_df = results_df[results_keep]

	# Get the number of agents in each location 
	results_val = [int(i) for i in results_df.iloc[-1,:]]

	# Find the total number of agents
	results_denom = sum(results_val)

	# Get the locations of the agents
	results_columns = list(results_df.columns)

	# Create two dicts, with 'location': # agents(or families)/ total num of agents (or families)

	truth_dict = dict(zip(truth_columns, [i/truth_denom for i in truth_val]))
	result_dict = dict(zip(results_columns, [i/results_denom for i in results_val]))

	error_list = []
	error_places = []

	# Now compare and see how we did

	for result_key, result_item in result_dict.items():
		if result_key in truth_dict:
			error = abs(truth_dict[result_key] - result_item)
			error_list.append(error)
			error_places.append(result_key)
		else:
			pass

	# Write the results to a csv
	#pd.DataFrame([error_places, error_list]).T.to_csv('errors_results.csv')

	# Return the mean absolute error to 3 places
	return round(np.mean(error_list), 3)



def go_test(args):
	'''	args_vals should be 
	[my_camp_weight, my_conflict_weight, 
					my_min_move, my_max_move,
					my_conflict_move_chance,
					my_camp_move_chance,
					my_default_move_chance]'''

	# first make sure args are valid, return large value if they are

	###### SET UP #####

	pd.DataFrame(args).T.to_csv('flee/my_settings.csv', 
		header = False, index = False, sep = "|")


	geog = InputGeography()
	geog.ReadLocationsFromCSV(FILES["truth_state_pops"])


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

	###### TRAINING #####

	for each_step in TEST_SET:

		candidate_zone = conflict_locations[conflict_locations['round'] == each_step]
		new_conflicts = set(candidate_zone.name)
		for i in new_conflicts:
			if i not in e.conflict_zone_names:
				e.add_conflict_zone(i)
		peace_transition = [i for i in lm_key if i not in new_conflicts ]
		for i in peace_transition:
			e.remove_conflict_zone(i)

		num_tot = {}

		for each_agent in range(0, 1000):
			place = np.random.randint(0, len(lm_key))
			e.addAgent(location=lm[lm_key[place]])

		e.refresh_conflict_weights()

		e.evolve()

		for each_location, loc_obj in lm.items():
			res_list[each_location].append(loc_obj.numAgents)


	###### CALCULATING ERROR #####

	results_df = pd.DataFrame(res_list)
	results_df.to_csv('test_results_of_sim.csv')

	# Get the validation values
	truth_df = pd.read_csv(FILES['truth_values'], skiprows =1, header = None)

	# Get the number of observed families
	truth_val = [int(i) for i in truth_df.iloc[-1, :]]

	# Get the total number of observed families
	truth_denom = sum(truth_val)

	# Get the locations of the families
	truth_columns = list(truth_df.iloc[0, :])

	# account for missing counts in truth 

	results_keep = [i for i in results_df.columns if i in truth_columns]

	results_df = results_df[results_keep]

	# Get the number of agents in each location 
	results_val = [int(i) for i in results_df.iloc[-1,:]]

	# Find the total number of agents
	results_denom = sum(results_val)

	# Get the locations of the agents
	results_columns = list(results_df.columns)

	# Create two dicts, with 'location': # agents(or families)/ total num of agents (or families)

	truth_dict = dict(zip(truth_columns, [i/truth_denom for i in truth_val]))
	result_dict = dict(zip(results_columns, [i/results_denom for i in results_val]))

	error_list = []
	error_places = []

	# Now compare and see how we did

	for result_key, result_item in result_dict.items():
		if result_key in truth_dict:
			error = abs(truth_dict[result_key] - result_item)
			error_list.append(error)
			error_places.append(result_key)
		else:
			pass

	# Write the results to a csv
	pd.DataFrame([error_places, error_list]).T.to_csv('test_errors_results.csv')

	# Return the mean absolute error
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
				"valid_state_pops": 'iom_dtm_reports/r89.csv',
				"valid_values": 'valid_vals.csv',
				"truth_state_pops": 'iom_dtm_reports/r89.csv',
				"truth_values": 'truth_vals.csv',
				}

	conflict_locations = pd.read_csv(FILES["conflict_locs"])
	num_rounds = len(set(conflict_locations['round']))

	#### The rounds we are examining ####
	train_start = 84
	train_end = 89
	test_start = 90
	test_end = 91

	TRAIN_SET = range(train_end - train_start)
	start_val = max(TRAIN_SET)
	TEST_SET = range(start_val, start_val + (test_end - test_start) + 1)

	s = Simulation()

	minimizer_kwargs = {"method": "BFGS"}

	x0 = [5, 0.2, 10, 10, 0.1, 0.1, 0.1]

	print("STARTING OPTIMIZATION")

	s.training.basinhopper(minimizer_kwargs, x0, niter=2)

	print("OPTIMIZATION RESULTS FOR BASINHOPPING: {} \nBEST PARAMS: {}\n".format(s.training.results['basinhopping'].message,
											s.training.results['basinhopping'].x))

	rranges = (slice(0,1,0.25), slice(0, 1, 0.25),
		slice(0, 100, 10), slice(0, 1000, 100),
		slice(0, 1.0, 0.25), slice(0, 1.0, 0.25),
		slice(0, 1.0, 0.25))

	s.training.brute(rranges)

	print("OPTIMIZATION RESULTS FOR BRUTE: {} \nBEST PARAMS: {}\n".format(s.training.results['brute'][0],
											s.training.results['brute'][1]))

	print("TESTING BASINHOP")
	s.testing(s.training.results['basinhopping'].x)

	print("TESTING BRUTE")
	s.testing(s.training.results['brute'][0])

	with open("results_summary.obj") as f:
		dump(s, f)


