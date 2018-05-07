from InputGeography import InputGeography
from flee.flee import Ecosystem

# plotting imports
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook


def go():
	geog = InputGeography()
	geog.ReadLocationsFromCSV('testing_locations_data.csv', 
							name_col = 0,
							population_col = 7 ,
							gps_x_col = 4,
							gps_y_col = 3)
	geog.ReadLinksFromCSV(csv_name = 'routes.csv',
							name1_col = 0,
							name2_col = 1,
							dist_col = 2)
	print("Geography loaded\n")

	e = Ecosystem()
	print("Ecosystem created\n")

	end_time = 10
	print("End time is: {}".format(end_time))

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

	for each_step in range(0,end_time):

		# this should be a list of locations, we add one to each
		# each agent will be a HH, based on outflow nums from IOM
		for each_agent in range(0, 100):
			place = np.random.randint(0, len(lm_key))
			e.addAgent(location=lm[lm_key[place]])

		e.evolve()

		e.printInfo()
		print("\n---------")
		print("\nTIME IS: {}".format(each_step))

		loc_list = []
		for each_location, loc_obj in lm.items():
			res_list[each_location].append(loc_obj.numAgents)

	results = pd.DataFrame(res_list)
	#results.columns = lm_key

	results.to_csv('simulation_results.csv')
	from plotter import read_datafile

	data = read_datafile("simulation_results.csv")

	x = data[:,0] # time
	y = data[:,1] # camp 22 (Mahama)
	z = data[:,2] # third column for comparison

	fig = plt.figure()
	ax1 = fig.add_subplot(111)

	ax1.set_title("Title")
	ax1.set_xlabel('Time')
	ax1.set_ylabel('No. of Refugees')

	ax1.plot(x,y, c='r')
	ax1.plot(x,z, c='b')

	leg = ax1.legend()

	plt.savefig('simres.png')



	# need to compare with some loss function


if __name__ == "__main__":
	go()