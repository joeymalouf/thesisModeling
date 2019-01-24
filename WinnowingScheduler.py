from mesa.time import BaseScheduler
import random

class WinnowingScheduler(BaseScheduler):

    def __init__(self, model, sample, percentage):
        super.__init__(self, model)
        self.sample = sample
        self.percentage = percentage
        self.currentStep = 0
    
    def step(self):
        """ Executes the step of all agents, one at a time, in
        random order.

        """
        if self.currentStep < self.sample:
            agent_keys = list(self._agents.keys())
            random.shuffle(agent_keys)

            for agent_key in agent_keys:
                self._agents[agent_key].step()
            self.steps += 1
            self.time += 1
            self.currentStep += 1
        else:
            self.currentStep = 0
            number_agents = (int)(len(self.agents)*self.percentage)
            
            for _ in range(number_agents):
                agent_to_remove = random.choice(self.agents)
                self.model.grid.remove_agent(agent_to_remove)
                self.remove(agent_to_remove)

            agent_keys = list(self._agents.keys())
            random.shuffle(agent_keys)

            for agent_key in agent_keys:
                self._agents[agent_key].step()
            self.steps += 1
            self.time += 1
            self.currentStep += 1
