from mesa import Agent, Model
from Molecule import Molecule
import random
import numpy as np

class Yeast(Agent):
    def __init__(self, unique_id, species_id, model, pos, reproduction_rate, energy, N, C):
        super().__init__(unique_id, model)
        self.pos = pos
        self.alive = True
        self.species_id = species_id
        self.reproduction_rate = reproduction_rate
        self.energy = energy
        self.neighbors = []
        self.N = N #.148
        self.C = C #1
        # self.O = O #.596
        # self.H = H #1.748
        self.C_to_reproduce = 90
        self.N_to_reproduce = 90*.148


    def ingest(self):
        NH3_injested = min(self.model.molecule_arrays[3][self.pos[0]][self.pos[1]], 1) * self.get_pH
        C6H12O6_injested = min(self.model.molecule_arrays[0][self.pos[0]][self.pos[1]], 1) * self.get_pH
        self.C += C6H12O6_injested 
        self.N += NH3_injested

        value = C6H12O6_injested * 50 + NH3_injested * 330 - 10
        self.model.molecule_arrays[0][self.pos[0]][self.pos[1]] -= C6H12O6_injested
        self.model.molecule_arrays[3][self.pos[0]][self.pos[1]] -= NH3_injested
        self.excrete(C6H12O6_injested)

        return value

        # "C6H12O6" = 0; "KNO2" = 1; "C02" = 2; "NH3" = 3
        # alga excrete 2 4

    def excrete(self, C6H12O6_injested):
        self.model.molecule_arrays[2][self.pos[0]][self.pos[1]] += .04

    
    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        self.model.microbe_count_by_species[self.species_id] -= 1

    def reproduce(self):
        possible_locations = self.model.grid.get_neighborhood(self.pos, include_center = False, radius = 1, moore = False)
        for location in possible_locations:
            if self.model.grid.is_cell_empty(location):
                mol = Yeast(self.model.next_id(), self.species_id, self.model, location, self.reproduction_rate, self.energy/4, self.N/2, self.C/2)
                self.model.schedule.add(mol)
                self.model.grid.place_agent(mol, location) 
                self.energy = self.energy/4
                self.model.microbe_count_by_species[self.species_id] += 1
                return
        return

    def step(self):
        self.ingest()
        if self.energy <= 0:
            self.die()
        if self.energy > self.reproduction_rate:
            self.reproduce()
    
    def get_pH(self):
        return np.e^(-((self.model.pH/2)-2)^2)
        
        
