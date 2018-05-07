from InputGeography import InputGeography
from flee.flee import Person, Location, Ecosystem

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
	for each_step in range(0,end_time):
		for each_agent in range(0, 100):
			place = np.random.randint(0, len(lm_key))
			e.addAgent(location=lm[lm_key[place]])


		e.evolve()

		e.printInfo()
		print("\n---------")
		print("\n\nTIME IS: {}".format(each_step))
		for each_location, loc_obj in lm.items():
			print(each_location, loc_obj.numAgents)


if __name__ == "__main__":
	go()