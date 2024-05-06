from parapy.core import *
import numpy as np


class Oxygen(Base):

    NumberOfOccupants = Input(1)

    @Attribute
    def oxygen_generation(self):
        og_volume = 2
        og_power = 350
        return og_volume, og_power

    @Attribute
    def get_oxygen_volume(self):
        return self.oxygen_generation[0] * np.ceil(self.NumberOfOccupants/5)

    @Attribute
    def get_oxygen_power(self):
        return self.oxygen_generation[1] * np.ceil(self.NumberOfOccupants/5)


if __name__ == '__main__':
    from parapy.gui import display
    obj = Oxygen(label='Oxygen')
    display(obj)
