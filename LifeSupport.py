from parapy.core import *
from Power import Power
from Water import Water
from Heating import Heating
from Oxygen import Oxygen
from Food import Food
import sys


class LifeSupport(Base):
    A_vertical = Input()
    A_base = Input()
    Q_sys = Input()
    Body = Input()

# Modules #

    sys.path.append('livingsupport_parts')

    @Part
    def Power(self):
        return Power(pass_down="Q_sys")

    @Part
    def Water(self):
        return Water()

    @Part
    def Heating(self):
        return Heating(pass_down="A_vertical, A_base, Q_sys,Body")

    @Part
    def Oxygen(self):
        return Oxygen()

    @Part
    def Food(self):
        return Food()

# Attributes #

    @Attribute
    def get_lifesup_volume(self):
        WatVol = self.Water.get_system_volume
        FarmVol = self.Food.get_farm_volume

        LifeSupportVolume = WatVol + FarmVol

        return LifeSupportVolume                # [m^3] Volume used by life support

    @Attribute
    def get_lifesup_power(self):
        #HeatPow = self.Heating.Q_heat
        OxyPow = self.Oxygen.OxygenSysPower
        FarmPow = self.Food.get_farm_power
        WatPow = self.Water.get_system_power

        LifeSupportPower = OxyPow + FarmPow + WatPow

        return LifeSupportPower                 # [W] Power used by life support


if __name__ == '__main__':
    from parapy.gui import display
    obj = LifeSupport(label='Life Support')
    display(obj)
