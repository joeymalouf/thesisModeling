class molecule_dto():

    def __init__(self, molecule_id, base_amount):
        # Name of the molecule
        self.molecule_id = molecule_id
        # Amount in each cell when simulation begins
        self.base_amount = base_amount