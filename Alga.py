from mesa import Agent, Model
from Molecule import Molecule
import random
import numpy as np

class Alga(Agent):
    def __init__(self, unique_id, species_id, model, pos, N, C):
        super().__init__(unique_id, model)
        self.pos = pos
        self.alive = True
        self.species_id = species_id
        self.N = N
        self.C = C
        self.C_to_reproduce = 540
        self.N_to_reproduce = 65.34
        self.neighbors = []

    def ingest(self):
        C02_ingested = min(self.model.molecule_arrays[2][self.pos[0]][self.pos[1]] * 250, 1) * max(.2, self.get_pH())
        NO2_ingested = min(self.model.molecule_arrays[1][self.pos[0]][self.pos[1]] * 500, 1)  * max(.2, self.get_pH())
        self.C += C02_ingested 
        self.N += NO2_ingested *.2
        self.model.molecule_arrays[1][self.pos[0]][self.pos[1]] -= NO2_ingested/14400
        self.model.molecule_arrays[2][self.pos[0]][self.pos[1]] -= C02_ingested/6000
        self.excrete(NO2_ingested)

        # "C6H12O6" = 0; "KNO2" = 1; "C02" = 2; "NH3" = 3
        # alga excrete 2 
    def decay(self):
        self.C = self.C - .0167*6
        self.N = self.N - .00202*6

    def excrete(self, NO2_ingested):
        self.model.molecule_arrays[3][self.pos[0]][self.pos[1]] += NO2_ingested*.8/14400
        # print("excrete alga: ", ( NO2_ingested*.5/360000))
    
    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        self.model.microbe_count_by_species[self.species_id] -= 1

    def reproduce(self):
        possible_locations = self.model.grid.get_neighborhood(self.pos, include_center = False, radius = 1, moore = False)
        for location in possible_locations:
            if self.model.grid.is_cell_empty(location):
                mol = Alga(self.model.next_id(), self.species_id, self.model, location, 56.87, 270)
                self.model.schedule.add(mol)
                self.model.grid.place_agent(mol, location) 
                self.C = 56.87
                self.N = 270
                self.model.microbe_count_by_species[self.species_id] += 1
                return
        return

    def step(self):
        self.ingest()
        self.decay()
        # print("Alga: ", self.get_pH())
        if self.C <= 0 or self.N <= 0:
            self.die()
        elif self.C > self.C_to_reproduce and self.N > self.N_to_reproduce:
            self.reproduce()
        elif self.C > self.C_to_reproduce*.6 and self.N > self.N_to_reproduce*.6:
            self.random_move()
        # p = random.randint(1,100)
        # if p > 90:
        #     print("carbon: ", self.C, " nitrogen: ", self.N)
             
    
    def get_pH(self):
        return np.e**(-((self.model.pH/2)-3.75)**2)
        
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