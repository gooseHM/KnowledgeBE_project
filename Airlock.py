from parapy.core import *


class Airlock(Base):
    NumberOfEVASuits = Input(2)                         # Number of EVA suits required
    EVASuitCapacity = Input(2)                          # Storage volume of 1 suit

    @Attribute
    def airlock_dims(self):
        Length = 7
        Width = 3
        Height = 3.5
        return Length, Width, Height

    @Attribute
    def get_airlock_volume(self):
        AirlockVolume = (self.airlock_dims[0]*self.airlock_dims[1]*self.airlock_dims[2]) + \
                        (self.NumberOfEVASuits*self.EVASuitCapacity)
        return AirlockVolume

    @Attribute
    def get_airlock_power(self):
        AirlockPower = 4500                             # [kWh] Airlock power consumption
        return AirlockPower


if __name__ == '__main__':
    from parapy.gui import display
    obj = Airlock(label='Airlock')
    display(obj)
