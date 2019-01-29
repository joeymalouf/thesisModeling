from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from Habitat import Habitat
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from microbe_dto import microbe_dto
from molecule_dto import molecule_dto
from Microbe import Microbe
from Molecule import Molecule
from mesa.datacollection import DataCollector

microbe_color = ["black", "orange", "green"]

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": .5,
        "Layer": 0,
    }
    portrayal["Color"] = microbe_color[agent.species_id]

    
    return portrayal

grid = CanvasGrid(agent_portrayal, 200, 200, 800, 800)


molecule_dtos = [molecule_dto("C6H12O6", 1000), molecule_dto("KNO2", 100), molecule_dto("C02", 0), molecule_dto("NH3", 0)]


chart = ChartModule(
    [{"Label": "Yeast", "Color": "Orange"},{"Label": "Alga", "Color": "Green"}],
    data_collector_name='datacollector'
)

pH = ChartModule(
    [{"Label": "pH", "Color": "red"}],
    data_collector_name='datacollector'
)

molecules = ChartModule(
    [{"Label": "C6H12O6", "Color": "red"},{"Label": "KNO2", "Color": "blue"},{"Label": "CO2", "Color": "Orange"},{"Label": "NH3", "Color": "cyan"}],
    data_collector_name='datacollector'
)

server = ModularServer(
    Habitat,
    [grid, chart, pH, molecules],
    "Mutalism Model",
    {"yeast": 200, "alga": 200, "molecule_dtos": molecule_dtos, "width": 200, "height": 200, "pH": 6.8}
)