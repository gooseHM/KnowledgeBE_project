from parapy.core import *


class Airlock(Base):
    NumberOfEVASuits = Input(3)                         # Number of EVA suits required
    AirlockVolume = Input(10)                            # [m^3] Airlock Volume
    AirlockPower = Input(10)                            # [kW] Airlock Power

    @Attribute
    def get_airlock_volume(self):
        AirlockVolume = self.AirlockVolume + self.NumberOfEVASuits
        return AirlockVolume


if __name__ == '__main__':
    from parapy.gui import display
    obj = Airlock(label='Airlock')
    display(obj)
