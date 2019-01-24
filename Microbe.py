from mesa import Agent, Model
from Molecule import Molecule
import random
import numpy as np

class Microbe(Agent):
    def __init__(self, unique_id, species_id, model, pos, growth_rate, reproduction_rate, intake_molecules, excrete_molecules):
        super().__init__(unique_id, model)
        self.pos = pos
        self.wellbeing = 100
        self.alive = True
        self.species_id = species_id
        self.growth_rate = growth_rate
        self.reproduction_rate = reproduction_rate
        self.intake_molecules = intake_molecules
        self.excrete_molecules = excrete_molecules
        self.neighbors = []

    def calculate_wellbeing(self):
        self.wellbeing += self.ingest() + self.microbe_interactions() + self.growth_rate

    def ingest(self):
        molecules = [food for food in self.adjacent if isinstance(food, Molecule) and food.molecule_id in self.intake_molecules]
        if len(molecules) > 0:
            mol = random.choice(molecules)
            mol.amount = mol.amount-1
            return mol.value
        molecules = [food for food in self.neighbors if isinstance(food, Molecule) and food.molecule_id in self.intake_molecules]
        if len(molecules) > 0:
            self.move_to_molecule(random.choice(molecules).pos)
            return 0
        else:
            self.random_move()
            return 0

    def excrete(self):
        possible_locations = self.model.grid.get_neighborhood(self.pos, include_center = False, radius = 1, moore = False)
        random.shuffle(possible_locations)
        for location in possible_locations:
            if self.model.grid.is_cell_empty(location):
                molecule_id = np.random.choice(self.excrete_molecules)
                mol = Molecule(self.model.next_id(), molecule_id, self.model, location, self.model.molecule_dict[molecule_id].energy, self.model.molecule_dict[molecule_id].amount)
                self.model.schedule.add(mol)
                self.model.grid.place_agent(mol, location)
                return  
        return
    
    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        self.model.microbe_count_by_species[self.species_id] -= 1

    def reproduce(self):
        possible_locations = self.model.grid.get_neighborhood(self.pos, include_center = False, radius = 1, moore = False)
        for location in possible_locations:
            if self.model.grid.is_cell_empty(location):
                mol = Microbe(self.model.next_id(), self.species_id, self.model, location, self.growth_rate, self.reproduction_rate, self.intake_molecules, self.excrete_molecules)
                self.model.schedule.add(mol)
                self.model.grid.place_agent(mol, location) 
                self.wellbeing = self.wellbeing/2
                self.model.microbe_count_by_species[self.species_id] += 1
                return
        return

    def step(self):
        self.adjacent = self.model.grid.get_neighbors(self.pos, include_center = True, radius = 1, moore = False)
        self.neighbors = self.model.grid.get_neighbors(self.pos, include_center = True, radius = 3, moore = False)
        self.calculate_wellbeing()
        if self.wellbeing <= 0:
            self.die()
        elif self.wellbeing > self.reproduction_rate:
            self.reproduce()
        elif self.wellbeing > 30:
            chance = random.choice([x for x in range(40)])
            if chance > 38:
                self.excrete()
        
    
    def microbe_interactions(self):
        return self.model.microbe_interaction_score(self.species_id)
        
    def move_to_molecule(self, pos):
        x_direction = 0
        if pos[0] > self.pos[0]:
            x_direction = 1
        elif pos[0] < self.pos[0]:
            x_direction = -1
        y_direction = 0
        if pos[1] > self.pos[1]:
            y_direction = 1
        elif pos[1] < self.pos[1]:
            y_direction = -1
        if self.model.grid.is_cell_empty([self.pos[0] + x_direction, self.pos[1]]):
            self.model.grid.move_agent(self, [self.pos[0] + x_direction, self.pos[1]])
        elif self.model.grid.is_cell_empty([self.pos[0], self.pos[1] + y_direction]):
            self.model.grid.move_agent(self, [self.pos[0], self.pos[1] + y_direction])
        return

    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore = True,
            include_center = False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)