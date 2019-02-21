from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from Yeast import Yeast
from Alga import Alga
from Molecule import Molecule
import random
import numpy as np
import scipy.signal
from fast_space import FastMultiGrid

class Habitat(Model):
    def __init__(self, yeast, alga, molecule_dtos, width, height, pH, steps):
        super().__init__()
        self.yeast = yeast
        self.alga = alga
        self.grid = FastMultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.steps = steps

        self.pH = pH
        self.filterA = np.array([[.0125, .0125, .0125],
                [.0125, .9, .0125],
                [.0125, .0125, .0125]])
        self.filterB = np.array([[.025, .025, .025],
                [.025, .8, .025],
                [.025, .025, .025]])
        self.filterC = np.array([[.05, .05, .05],
                [.05, .6, .05],
                [.05, .05, .05]])
        self.filterD = np.array([[.075, .075, .075],
                [.075, .4, .075],
                [.075, .075, .075]])
        self.filterE = np.array([[.1, .1, .1],
                [.1, .2, .1],
                [.1, .1, .1]])

        self.molecule_arrays = np.zeros((len(molecule_dtos),width,height))
        self.molecules = molecule_dtos
        self.molecule_dict = {}

        # "C6H12O6" = 0; "KNO2" = 1; "C02" = 2; "NH3" = 3

        for i in range(len(molecule_dtos)):
            self.molecule_dict[i] = self.molecules[i].molecule_id
            self.molecule_arrays[i] += self.molecules[i].base_amount

        self.microbe_count_by_species = {1:0, 2:0}
        self.microbe_dict = {1: "Yeast", 2: "Alga"}

        for _ in range(self.yeast):
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            pos = [x, y]
            N = random.randint(4, 10)
            C = random.randint(22, 66)
            a = Yeast(self.next_id(), 1, self, pos, N, C)
            self.schedule.add(a)
            self.grid.place_agent(a, (x, y))
            self.microbe_count_by_species[1] += 1
        
        for _ in range(self.alga):
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            pos = [x, y]
            N = random.randint(28, 85)
            C = random.randint(135, 405)
            a = Alga(self.next_id(), 2, self, pos, N, C)
            self.schedule.add(a)
            self.grid.place_agent(a, (x, y))   
            self.microbe_count_by_species[2] += 1


        self.datacollector = DataCollector(
            model_reporters={"Yeast" : species1_count, "Alga" : species2_count, "pH" : get_pH, "C6H12O6" : avg_C6H12O6, "KNO2" : avg_KNO2, "CO2" : avg_CO2, "NH3" : avg_NH3})
        self.datacollector.collect(self)

        self.step()

    def step(self):
        self.pH = self.calculate_pH()
        for i in range(len(self.molecule_arrays)):
            self.molecule_arrays[i] = scipy.signal.convolve2d(self.molecule_arrays[i], self.filterE, mode='same', boundary='wrap')
        self.datacollector.collect(self)
        self.schedule.step()
        if self.schedule.steps % 50 == 0:
            print("Step: ", self.schedule.steps)
            print("Alga: ", self.microbe_count_by_species[2])
            print("Yeast: ", self.microbe_count_by_species[1])
        if (self.schedule.steps > self.steps):
            self.running = False
        

    def calculate_pH(self):
        return max(0, min(14, self.pH + -10**-7 * self.microbe_count_by_species[1] + 10**-7 * self.microbe_count_by_species[2]))

def species1_count(model):
    return model.microbe_count_by_species[1]

def species2_count(model):
    return model.microbe_count_by_species[2]
    
def get_pH(model):
    return model.pH

def avg_C6H12O6(model):
    return model.molecule_arrays[0].mean()

def avg_KNO2(model):
    return model.molecule_arrays[1].mean()

def avg_CO2(model):
    return model.molecule_arrays[2].mean()

def avg_NH3(model):
    return model.molecule_arrays[3].mean()