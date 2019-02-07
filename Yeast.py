from mesa import Agent, Model
from Molecule import Molecule
import random
import numpy as np

class Yeast(Agent):
    def __init__(self, unique_id, species_id, model, pos, N, C):
        super().__init__(unique_id, model)
        self.pos = pos
        self.alive = True
        self.species_id = species_id
        self.neighbors = []
        self.N = N #.148
        self.C = C #1
        # self.O = O #.596
        # self.H = H #1.748
        self.C_to_reproduce = 90
        self.N_to_reproduce = 90*.148


    def ingest(self):
        NH3_ingested = min(self.model.molecule_arrays[3][self.pos[0]][self.pos[1]], 1) * (.7 + (self.get_pH()*.3))
        C6H12O6_ingested = min(self.model.molecule_arrays[0][self.pos[0]][self.pos[1]], 222)/222 * (.7 + (self.get_pH()*.3))
        self.C += C6H12O6_ingested 
        self.N += NH3_ingested

        self.model.molecule_arrays[0][self.pos[0]][self.pos[1]] -= C6H12O6_ingested
        self.model.molecule_arrays[3][self.pos[0]][self.pos[1]] -= NH3_ingested
        self.excrete(C6H12O6_ingested)

        # "C6H12O6" = 0; "KNO2" = 1; "C02" = 2; "NH3" = 3
        # alga excrete 2 4

    def decay(self):
        self.C = self.C - .1/6
        self.N = self.N - .1 * .148 /6

    def excrete(self, C6H12O6_ingested):
        self.model.molecule_arrays[2][self.pos[0]][self.pos[1]] += (.7 + (self.get_pH()*.3)) * (2.0/3.0) /6
        # print("excrete yeast: ", (.7 + (self.get_pH()*.3)))
    
    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        self.model.microbe_count_by_species[self.species_id] -= 1

    def reproduce(self):
        possible_locations = self.model.grid.get_neighborhood(self.pos, include_center = False, radius = 1, moore = False)
        for location in possible_locations:
            if self.model.grid.is_cell_empty(location):
                mol = Yeast(self.model.next_id(), self.species_id, self.model, location, 6.66, 45)
                self.model.schedule.add(mol)
                self.model.grid.place_agent(mol, location) 
                self.C = 45
                self.N = 6.66
                self.model.microbe_count_by_species[self.species_id] += 1
                return
        return

    def step(self):
        self.ingest()
        self.decay()
        if self.C <= 0 or self.N <= 0:
            self.die()
        elif self.C > self.C_to_reproduce and self.N > self.N_to_reproduce:
            self.reproduce()
        # p = random.randint(1,100)
        # if p > 90:
        #     print("carbon: ", self.C, " nitrogen: ", self.N)
    
    def get_pH(self):
        return np.e**(-((self.model.pH/2)-2)**2)
        
        
