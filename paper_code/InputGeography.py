import csv
import flee
import pandas as pd

class InputGeography:
  """
  Class which reads in Geographic information.
  """
  def __init__(self):
    self.locations = []
    self.links = []


  def ReadLocationsFromCSV(self,csv_name):
    """
    Converts a CSV file to a locations information table 
    """
    self.locations = []

    df = pd.read_csv(csv_name)

    for row in df.itertuples():

      self.locations.append([row.name, row.pop, row.lon, row.lat])


  def ReadLinksFromCSV(self,csv_name):
    """
    Converts a CSV file to a locations information table 
    """
    self.links = []

    df = pd.read_csv(csv_name)

    for row in df.itertuples():

        self.links.append([row.start, row.end, row.dist])

  def StoreInputGeographyInEcosystem(self, e):
    """
    Store the geographic information in this class in a FLEE simulation, 
    overwriting existing entries.
    """
    lm = {}

    for l in self.locations:
      lm[l[0]] = e.addLocation(l[0], movechance=0.3, pop=int(l[1]), x=l[2], y=l[3])

    for l in self.links:
        e.linkUp(l[0], l[1], int(l[2]))

    return e, lm

