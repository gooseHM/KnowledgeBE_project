from parapy.core import *


class Water(Base):
    WaterProduction = Input(1)                           # [L/min] Water production
    StorageCapacity = Input(10)                          # [L] Water Storage Capacity
    StorageVolume = Input(10)                            # [m^3] Water storage tank volume


if __name__ == '__main__':
    from parapy.gui import display
    obj = Water(label='Water')
    display(obj)
