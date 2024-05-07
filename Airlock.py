from parapy.core import *


class Airlock(Base):
    NumberOfEVASuits = Input(2)                         # Number of EVA suits required
    EVASuitCapacity = Input(2)                          # Storage volume of 1 suit

    @Attribute
    def airlock_dims(self):
        length = 7
        width = 3
        height = 3.5
        return length, width, height

    @Attribute
    def get_airlock_volume(self):
        airlock_volume = (self.airlock_dims[0]*self.airlock_dims[1]*self.airlock_dims[2]) + \
                        (self.NumberOfEVASuits*self.EVASuitCapacity)
        return airlock_volume

    @Attribute
    def get_airlock_power(self):
        airlock_power = 4500
        return airlock_power


if __name__ == '__main__':
    from parapy.gui import display
    obj = Airlock(label='Airlock')
    display(obj)
