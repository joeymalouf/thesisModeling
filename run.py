from Habitat import Habitat
from molecule_dto import molecule_dto
from server import server
import matplotlib.pyplot as plt

# "C6H12O6" = 0; "KNO2" = 1; "C02" = 2; "NH3" = 3
# M. P. Azuara, P. J. Aparicio, Plant Physiol. 71, 286–290 (1983)

molecule_dtos = []
molecule_dtos.append(molecule_dto("C6H12O6", .02))
molecule_dtos.append(molecule_dto("KNO2", .002))
molecule_dtos.append(molecule_dto("C02", .001))
molecule_dtos.append(molecule_dto("NH3", 0))


H = Habitat(40, 40, molecule_dtos, 300, 300, 6.8, 10000)
H.run_model()

data = H.datacollector.get_model_vars_dataframe()

yeast = data["Yeast"].values
alga = data["Alga"].values
pH = data["pH"].values
C6H12O6 = data["C6H12O6"].values
KNO2 = data["KNO2"].values
CO2 = data["CO2"].values
NH3 = data["NH3"].values

print(data)


fig = plt.figure(1)
fig.subplots_adjust(hspace=1)
a = plt.subplot(3,2,1)
plt.title("Microbes")
plt.ylabel("microbes")
plt.xlabel("Step")
plt.yscale("log")
plt.plot(yeast, 'orange')
plt.plot(alga, 'g')
b = plt.subplot(3,2,2)
plt.title("pH")
plt.plot(pH)
c = plt.subplot(3,2,3)
plt.title("C6H12O6")
plt.plot(C6H12O6)
d = plt.subplot(3,2,4)
plt.title("KNO2")
plt.plot(KNO2)
e = plt.subplot(3,2,5)
plt.title("CO2")
plt.plot(CO2)
f = plt.subplot(3,2,6)
plt.title("NH3")
plt.plot(NH3)
plt.show()


# server.port = 8888
# server.launch()