from parapy.core import *
import numpy as np


class Oxygen(Base):

    NumberOfOccupants = Input(1)

    @Attribute
    def oxygen_generation_system(self):
        ogs_volume = 2
        ogs_power = 350
        return ogs_volume, ogs_power

    @Attribute
    def get_oxygen_volume(self):
        return self.oxygen_generation_system[0] * np.ceil(self.NumberOfOccupants/5)

    @Attribute
    def get_oxygen_power(self):
        return self.oxygen_generation_system[1] * np.ceil(self.NumberOfOccupants/5)


if __name__ == '__main__':
    from parapy.gui import display
    obj = Oxygen(label='Oxygen')
    display(obj)
