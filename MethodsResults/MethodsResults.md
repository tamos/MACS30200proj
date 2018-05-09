#### Data

The principal data sources for this analysis are: (i) records of the volume and geographic distribution of internally displaced people collected by the International Organization for Migration (IOM); (ii) records of violent incidents from the Armed Conflict Location and Event Database (ACLED); (iii) spatial data for populated locations from the United Nations Office for the Coordination of Humanitarian Affairs (UNOCHA). ^[Links to download all data files are available in the Appendix.]

_IOM Displacement Tracking Matrix (DTM)_

IOM conducts regular surveys of the location and number of displaced households in Iraq. Surveys are conducted approximately every two weeks as part of IOM's assessment system. ^[See @iommethods for details of the survey methodology.] For this simulation, the IDP Master Lists for rounds 84 (November 29, 2017) through 91 (April 30, 2018) were used. 

IDP Master Lists have consistent formats across rounds, which motivated their selection over more granular round-specific reports. Each Master List provides updated figures of the number of households at each reported location, as well as adding new locations as they are surveyed. Master Lists were downloaded as MS Excel documents and converted to CSV format.

_Armed Conflict Location and Event Database (ACLED)_

ACLED is an initiative which catalogues incidents of violence across a number of countries. ACLED data are frequently used by researchers studying conflict/crisis. For this simulation, ACLED data for Iraq was accessed from the Humanitarian Data Exchange portal's live update link as a CSV. [@humdata]

For each event, ACLED records the approximate location, date and time, estimated fatalities, a short description, as well as other features. This simulation uses the approximate location and the time in the simulation environment. Events with no estimated fatalities were removed from the data under the assumption they are not indicative of a level of conflict sufficient to provoke new displacements. 

_Populated Locations in Iraq_

Spatial data on the location of populated places in Iraq was collected from UNOCHA, via the HumData portal in ShapeFile format. [@unochaspatial] This dataset was chosen specifically as it is compatible with the Displacement Tracking Matrix and is derived from IOM's internal placename database. It provides the names and locations of not only official settlements, but neighbourhoods and other unofficial locations. 

<center>
| Source | Variable |  Start |  End | 
|---|---|---|---|---|
| IOM | IDP Location |  2017-11-29 | 2018-04-30 |
| IOM | IDP Population |  2017-22-29 | 2018-04-30 |
| ACLED | Location Type |  2017-01-01 | 2018-04-28 |
| UNOCHA | Network Node Location | NA  | NA  | 
</center>

_Data Joining and Aggregation_ ^[Algorithms used to perform these operations are available in the Appendix.]

To align the three data sources in the desired format, a series of aggregation and spatial join operations were performed. The spatial geometries of IDP, event, and populated places were transformed into representative polygons using the GeoPandas convex hull functionality after being aggregated to the level of the first sub-national administrative region (governorate/province). On these transformed datasets, two sets of spatial joins were used. First, the populated locations were joined with the observed IDP populations data. Population numbers were summed by region to establish the initial and future populations of each location. Second, the populated locations, aggregated to the regional level and represented geometrically as a convex hull, were joined with ACLED records involving at least one fatality. Population location geometries were then transformed into centroids for use as node locations. Lastly, the distance between these centroids was calculated using the GeoPandas `distance` function.

These joins and aggregation produced four datasets:
	- population centres represented as a point, with starting IDP populations (nodes)
	- final observed IDP populations by population centre
	- conflict locations and their date of observation
	- distance between all population centres (edges)


#### Models and Methods

- Household vs individual
why household?

_Agent-based Models_

Agent-based simulations require the modeller to specify all rules by which individuals make decisions. This makes explicit the connection between results and theory. In a displacement simulation, agents (a household or individual) move across a virtual space and interact with elements of the simulation according to some set of rules. ^[See @edwardschaos for an accessible explanation of agent-based models.] Beyond its proven ability to model a wide range of phenomena, this approach is intuitively understood by non-technical audiences and is relatively simple to implement. 

Many of the critiques of simulation generally, such as those from Maldonado and Greenland [-@maldonadosimulationcritical] apply to agent-based models in particular. The rules by which agents "live" may be unreasonable simplifications or require bold assumptions which, in the worst case, limit simulation results' generalizability to just other simulations. This is notable given one of the reasons for choosing simulation methods is to manipulate virtual ecosystems that enhance understanding of reality.

_The FLEE Agent-based Modelling Environment_

FLEE is a purpose-built Agent-based Modelling (ABM) environment for simulating the flow of people. The initial development of the environment has focused on modelling forced displacement, specifically refugee movements. In FLEE, agents traverse a network where each node represents a town, camp, or conflict. Agents follow a series of rules in order to determine where they will travel where conflict and distant locations are less likely to be selected, and non-conflict and proximate locations are more likely. In this simulation, there were seven possible parameters which could be adjusted.

<center>
#### Parameters Varied In the Simulation
| Name | Description  | 
|---|---|---|---|---|
| `CampWeight`  | The factor by which camps 'attract' agents. |  
| `ConflictWeight` | Reduction factor for camps. |
|  `MinMoveSpeed` | Minimum distance an agent covers in one step. | 
|  `MaxMoveSpeed` |  Maximum distance an agent covers in one step. |
|  `ConflictMoveChance` |  Default probability for leaving a conflict zone. |
|  `CampMoveChance` |  Default probability for leaving a camp. |
|  `DefaultMoveChance` |  Default probability for leaving any location. |
</center>

Apart from these parameters, the simulation was set so that agents introduced added to existing populations (`TakeRefugeesFromPopulation = False`), camp weights were dynamically calculated based on the agent population in the camp at each step (`UseDynamicCampWeights = True`), agent awareness was limited to their location (`AwarenessLevel = 1`), IDP mode was enabled (`UseIDPMode = True`), and agents did not accumulate knowledge about the network over time (`UseDynamicAwareness = False`).

_framework structure, algorithm_


_Random Walks_

The movement of displaced people can be thought of as a random walk, where displaced people move between points according to some set of probabilities defined by a specified function. ^[One well-known example is Lévy flight.] This approach is used to model the movement of animal populations in biology and everyday human movement. [@codlingrandomwalks; @bovet1988spatial; @gallotti2016stochastic] It may have some application in the study of forced migration - a random walk simulation from the International Organziation for Migration reportedly predicts displacement trends with error rates less than 10%. [@iomrandomwalk] ^[This claim is yet to be tested in a peer-reviewed publication.]

For their apparent robustness, random walks have questionable theoretical value for research in forced migration. If a process of forced migration is in fact a random walk, how does one interpret the results of a given simulation? What do simulation results say about the experience of displaced people? To the author's knowledge, there is no systematic way to interpret random walks to answer such questions. Nevertheless, random walks' ability to "blindly" model real phenomena makes them useful as a benchmark against which to compare more sophisticated models - a "uniform probability plus" of sorts. If a random walk outperforms more theoretically-informed models, this should be interpreted as weakness in the sophisticated model, rather than support of any "chaos" theory of forced migration. 


_simulation set up and iteration_

_optimization attempts_

#### Results


\pagebreak

# Appendix

#### Data Sources

IOM Displacement Tracking Matrix: http://iraqdtm.iom.int 

Populated Places in Iraq: https://data.humdata.org/dataset/settlements-villages-towns-cities 

Iraq Administrative Boundaries: https://data.humdata.org/dataset/iraq-admin-level-1-boundaries ^[This data was used for visualization purposes only.]

ACLED Event Data: https://www.acleddata.com/data/ 

ACLED Data is also available with live updates from: www.data.humdata.org

#### Algorithms 

_Aggregation of Populated Locations_

	generate spatial geometries of all populated locations
	dissolve geometries by Governorate
	convert geometries to convex hulls
	spatial join with second dataset (if needed)

_Creation of new geometries_

	load non-spatial data with requisite spatial features (lat, lon)
	for each lat, lon pair
		create geometry
	assign new geometries as a feature of the dataset

_Calculation of edge lengths_

	load dissolved geometries of Populated Locations
	convert geometries to centroids (a single point)
	for each row
		calculate the distance between the row's geometry and all other geometries
		convert distances to an integer value
		for each trip
			if the start and end are equal
				move to the next trip
			if the trip has not yet been seen
				add the trip to a master trip list
				write the start, end, and distance to a file
			

_Identification of Conflict Zones_

	load ACLED conflict data
	remove cases with no fatalities
	create new geometries (above)
	sort by event date
	convert event dates to integers
	remove cases with event dates before the lower date bound
	remove cases with event dates after the upper date bound
	assign round number, equivalent to step in simulation
	write location names and steps to file


_Creation of test dataset_

	aggregate population locations
	load final observed dataset
	create geometries for final observed dataset
	spatial join observed counts with population locations
	sum observed counts by governorate
	write to file


\newpage
#### Figures

![Iraq Populated Places with level 1 administrative boundaries. Source: UNOCHA ](PopulatedLocations.png)



\pagebreak
# References

---
title: "Simulating Forced Migration with the Flee Agent-based Modelling Environment "
author: Tyler Amos
date: 9 May 2018
abstract: "This is a summary of initial results for a simulation of forced migration, specifically internal displacement. Iraq in the period January 2017 through to April 2018 is used as a case study. "

bibliography: Simulating-Displacement-MethodsResults.bib
    
---

[compile and install instructions]: <> ( To compile run in shell: pandoc inputfilename -o outputfilename --filter pandoc-citeproc
To install pandoc-citeproc: brew install pandoc pandoc-citeproc 
To install latex: brew install caskroom/cask/basictex 
Ref: https://stackoverflow.com/questions/4823468/comments-in-markdown#20885980
Ref: http://www.chriskrycho.com/2015/academic-markdown-and-citations.html
Ref: https://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)