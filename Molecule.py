from mesa import Agent, Model
import random

class Molecule(Agent):

    def __init__(self, unique_id, molecule_id, model, pos, value, amount):
        super().__init__(unique_id, model)
        self.pos = pos
        self.value = value
        self.alive = True
        self.molecule_id = molecule_id
        self.amount = amount

    def step(self):
        if self.amount <= 0:
            self.remove()
    
    def remove(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)