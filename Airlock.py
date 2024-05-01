from parapy.core import *


class Airlock(Base):
    NumberOfEVASuits = Input(2)                         # Number of EVA suits required
    EVASuitCapacity = Input(2)                          # Storage volume of 1 suit

    @Attribute
    def airlock_dims(self):
        Length = 7
        Width = 3
        Height = 3
        return Length, Width, Height

    @Attribute
    def get_airlock_volume(self):
        AirlockVolume = (self.Length*self.Width*self.Height) + (self.NumberOfEVASuits*self.EVASuitCapacity)
        return AirlockVolume


if __name__ == '__main__':
    from parapy.gui import display
    obj = Airlock(label='Airlock')
    display(obj)
