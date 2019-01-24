from mesa import Agent, Model
from Molecule import Molecule
import random
import numpy as np

class Alga(Agent):
    def __init__(self, unique_id, species_id, model, pos, reproduction_rate, energy):
        super().__init__(unique_id, model)
        self.pos = pos
        self.alive = True
        self.species_id = species_id
        self.reproduction_rate = reproduction_rate
        self.energy = energy
        self.neighbors = []

    def calculate_energy(self):
        self.energy += self.ingest() * self.get_pH()

    def ingest(self):
        C02_injested = min(self.model.molecule_arrays[2][self.pos[0]][self.pos[1]], .2)
        NO2_injested = min(self.model.molecule_arrays[1][self.pos[0]][self.pos[1]] * .002, .02)
        value = NO2_injested * 500 + C02_injested * 330 - 10
        self.model.molecule_arrays[1][self.pos[0]][self.pos[1]] -= NO2_injested
        self.model.molecule_arrays[2][self.pos[0]][self.pos[1]] -= C02_injested
        self.excrete(NO2_injested)

        return value

        # "C6H12O6" = 0; "KNO2" = 1; "C02" = 2; "NH3" = 3
        # alga excrete 2 

    def excrete(self, NO2_injested):
        p = random.randint(0, 100)
        if p < (NO2_injested * 5000):
            self.model.molecule_arrays[3][self.pos[0]][self.pos[1]] += .02
    
    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        self.model.microbe_count_by_species[self.species_id] -= 1

    def reproduce(self):
        possible_locations = self.model.grid.get_neighborhood(self.pos, include_center = False, radius = 1, moore = False)
        for location in possible_locations:
            if self.model.grid.is_cell_empty(location):
                mol = Alga(self.model.next_id(), self.species_id, self.model, location, self.reproduction_rate, self.energy/4)
                self.model.schedule.add(mol)
                self.model.grid.place_agent(mol, location) 
                self.energy = self.energy/4
                self.model.microbe_count_by_species[self.species_id] += 1
                return
        return

    def step(self):
        self.calculate_energy()       
        if self.energy <= 0:
            self.die()
        elif self.energy > self.reproduction_rate:
            self.reproduce()
        elif self.energy > 70:
            self.random_move()
             
    
    def get_pH(self):
        return -.08*((self.model.pH-8)**2) + 1
        
    # def move_to_molecule(self, pos):
    #     x_direction = 0
    #     if pos[0] > self.pos[0]:
    #         x_direction = 1
    #     elif pos[0] < self.pos[0]:
    #         x_direction = -1
    #     y_direction = 0
    #     if pos[1] > self.pos[1]:
    #         y_direction = 1
    #     elif pos[1] < self.pos[1]:
    #         y_direction = -1
    #     if self.model.grid.is_cell_empty([self.pos[0] + x_direction, self.pos[1]]):
    #         self.model.grid.move_agent(self, [self.pos[0] + x_direction, self.pos[1]])
    #     elif self.model.grid.is_cell_empty([self.pos[0], self.pos[1] + y_direction]):
    #         self.model.grid.move_agent(self, [self.pos[0], self.pos[1] + y_direction])
    #     return

    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore = True,
            include_center = False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)