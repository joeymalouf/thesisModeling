from Habitat import Habitat
from molecule_dto import molecule_dto
from server import server

# "C6H12O6" = 0; "KNO2" = 1; "C02" = 2; "NH3" = 3

# molecule_dtos = []
# molecule_dtos.append(molecule_dto("C6H12O6", 1))
# molecule_dtos.append(molecule_dto("KNO2", 1))
# molecule_dtos.append(molecule_dto("C02", 1))
# molecule_dtos.append(molecule_dto("NH3", 1))


# H = Habitat(200, 200, molecule_dtos, 400, 400, 6.0)
# H.run_model()


server.port = 8888
server.launch()