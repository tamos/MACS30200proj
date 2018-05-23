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
from scipy.optimize import minimize
import pickle



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

	def vanilla_minimizer(self, start, **kwargs):
		self.results['vanilla_minimizer'] = minimize(go, start, **kwargs)

def go_test(args):

	'''	args_vals should be 
	[my_camp_weight, my_conflict_weight, 
					my_min_move, my_max_move,
					my_conflict_move_chance,
					my_camp_move_chance,
					my_default_move_chance]'''

	# first make sure args are valid
	if bad_args(args):
		raise ValueError

	###### SET UP #####

	pd.DataFrame(args).T.to_csv('flee/my_settings.csv', 
		header = False, index = False, sep = "|")


	geog = InputGeography()
	geog.ReadLocationsFromCSV(FILES["test_locs_init"])


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

	# step 1: Get the forecast error

	results_df = pd.DataFrame(res_list)
	results_df.to_csv('test_raw_results_of_sim.csv')

	# Get the validation values
	truth_df = pd.read_csv(FILES['test_file'])
	init_df = pd.read_csv(FILES['test_locs_init'], usecols = ['name', 'pop'])

	truth_dict = {}
	step = 0
	for each_row in truth_df.itertuples():
		truth_dict[step] = sum(each_row[1:])
		step += 1


	results_tmp = []
	step = 0
	for each_row in results_df.itertuples():
		each_row = each_row[1:]
		results_tmp.append([(i/sum(each_row)) * truth_dict[step] for i in each_row])
		step += 1

	results_df = pd.DataFrame(results_tmp)

	forecast_error = abs(truth_df.values - results_df.values)

	# step 2: get the mean absolute error

	new_truth = []
	first_row = list(init_df['pop'])
	new_truth.append(first_row)
	for i in truth_df.values:
		new_truth.append(list(i))
	new_truth = np.array(new_truth)

	new_truth = new_truth[:-1]

	results_tmp = results_df.values
	yt_less_ytminus1 = abs(results_tmp - new_truth)

	mean_absolute_error = yt_less_ytminus1.sum() / (results_tmp.shape[0]-1)

	# step 3: calculate MASE

	fore_adj = forecast_error/mean_absolute_error
	MASE = fore_adj.sum()/results_tmp.shape[0]

	# step 4: track  MASE over time

	print("{}|{}".format("|".join([str(i) for i in args]), MASE))
	return MASE 


def go(args):

	'''	args_vals should be 
	[my_camp_weight, my_conflict_weight, 
					my_min_move, my_max_move,
					my_conflict_move_chance,
					my_camp_move_chance,
					my_default_move_chance]'''

	# first make sure args are valid, return large error if they aren't
	if bad_args(args):
		return .9 * 1000

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

	# step 1: Get the forecast error

	results_df = pd.DataFrame(res_list)
	results_df.to_csv('raw_results_of_sim.csv')

	# Get the validation values
	truth_df = pd.read_csv(FILES['training_file'])
	init_df = pd.read_csv(FILES['locations_init'], usecols = ['name', 'pop'])

	truth_dict = {}
	step = 0
	for each_row in truth_df.itertuples():
		truth_dict[step] = sum(each_row[1:])
		step += 1


	results_tmp = []
	step = 0
	for each_row in results_df.itertuples():
		each_row = each_row[1:]
		results_tmp.append([(i/sum(each_row)) * truth_dict[step] for i in each_row])
		step += 1

	results_df = pd.DataFrame(results_tmp)

	forecast_error = abs(truth_df.values - results_df.values)

	# step 2: get the mean absolute error

	new_truth = []
	first_row = list(init_df['pop'])
	new_truth.append(first_row)
	for i in truth_df.values:
		new_truth.append(list(i))
	new_truth = np.array(new_truth)

	new_truth = new_truth[:-1]

	results_tmp = results_df.values
	yt_less_ytminus1 = abs(results_tmp - new_truth)

	mean_absolute_error = yt_less_ytminus1.sum() / (results_tmp.shape[0]-1)

	# step 3: calculate MASE

	fore_adj = forecast_error/mean_absolute_error
	MASE = fore_adj.sum()/results_tmp.shape[0]

	# step 4: track  MASE over time

	print("{}|{}".format("|".join([str(i) for i in args]), MASE))
	return MASE * 1000


def bad_args(args):
	# make sure min and max are in right order
	if args[2] > args[3]:
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


if __name__ == "__main__":

	x0 = [1.0, # my_camp_weight
		 0.25, # my_conflict_weight
		0.5, # my_min_move
		5.0, # my_max_move
		1.0, # my_conflict_move_chance
		0.1, # my_camp_move_chance
		0.3] # my_default_move_chance

	# from https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict

	with open('file_locs.pickle', 'rb') as f:
		FILES = pickle.load(f)

	conflict_locations = pd.read_csv(FILES["conflict_locs"])
	num_rounds = len(set(conflict_locations['round']))

	#### The rounds we are examining, with their key form Datasets.py ####
	train_start = 84 # this should match 'observed_pop_init'
	train_end = 88 # this should match 'valid_state_pops'
	test_start = 89 # this should match 'test_pop_init'
	test_end = 91 # this should match 'test_final_pops'

	TRAIN_SET = range(train_end - train_start)
	start_val = max(TRAIN_SET)
	TEST_SET = range(start_val, start_val + (test_end - test_start) + 1)

	s = Simulation()

	#### OPTIMIZATION ####

	print("STARTING OPTIMIZATION")

	###############################
	#### BASINHOPPER ALGORITHM ####
	###############################

	#minimizer_kwargs = {"method": "BFGS"}

	#s.training.basinhopper(minimizer_kwargs, x0, niter=2)

	#print("OPTIMIZATION RESULTS FOR BASINHOPPING: {} \nBEST PARAMS: {}\n".format(s.training.results['basinhopping'].message,
											#s.training.results['basinhopping'].x))

	#print("TESTING BASINHOP")
	#s.testing(s.training.results['basinhopping'].x)

	#with open("basin_results_summary.obj", 'wb') as f:
		#pickle.dump(s, f)

	###############################
	#### BRUTE FORCE ALGORITHM ####
	###############################

	#rranges = (slice(0.1,1,0.25), slice(0.001, 1, 0.25),
		#slice(0.001, 100, 10), slice(0.01, 1000, 100),
		#slice(0.001, 1.0, 0.25), slice(0.01, 1.0, 0.25),
		#slice(0.001, 1.0, 0.25))

	#s.training.brute(rranges)

	#print("OPTIMIZATION RESULTS FOR BRUTE: {} \nBEST PARAMS: {}\n".format(s.training.results['brute'][0],
											#s.training.results['brute'][1]))

	#print("TESTING BRUTE")
	#s.testing(s.training.results['brute'][0])

	#with open("brute_results_summary.obj", 'wb') as f:
		#pickle.dump(s, f)

	###########################
	#### SIMPLE MINIMIZER ####
	###########################

	#s.training.vanilla_minimizer(x0)

	#print("OPTIMIZATION RESULTS FOR VANILLA MINIMIZER: {} \nBEST PARAMS: {}\n".format(s.training.results['vanilla_minimizer'].message,
											#s.training.results['vanilla_minimizer'].x))

	#print("TESTING VANILLA MINIMIZER")

	#s.testing.test(s.training.results['vanilla_minimizer'].x)
	
	#with open("vanilla_results_summary.obj", 'wb') as f:
		#pickle.dump(s, f)


