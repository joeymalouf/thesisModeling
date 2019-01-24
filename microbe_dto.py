class microbe_dto():

    def __init__(self, species_id, reproduction_rate, growth_rate, intake_molecules, excrete_molecules, quantity):
        # Name species_id whatever you want, string or int
        self.species_id = species_id
        # Reproduction rate is the number of 'points' it needs to reproduce
        self.reproduction_rate = reproduction_rate
        # Growth rate is the number of 'points' it gains intrinsically each step
        self.growth_rate = growth_rate
        # List of molecules it can ingest
        self.intake_molecules = intake_molecules
        # List of molecules it can excrete
        self.excrete_molecules = excrete_molecules
        # How many microbes of this type you want
        self.quantity = quantity