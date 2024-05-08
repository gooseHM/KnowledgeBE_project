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
    NumberOfOccupants = Input()
    MissionDuration = Input()
    Q_heat = Input()
# Modules #

    @Part
    def Power(self):
        return Power(pass_down="Q_sys, Body,Q_heat")

    @Part
    def Water(self):
        return Water(FarmVolume=self.Food.get_farm_volume, pass_down=("NumberOfOccupants", "MissionDuration"))

    @Part
    def Heating(self):
        return Heating(pass_down="A_vertical, A_base, Q_sys,Body")

    @Part
    def Oxygen(self):
        return Oxygen(pass_down="NumberOfOccupants")

    @Part
    def Food(self):
        return Food(pass_down=("NumberOfOccupants", "MissionDuration"))

# Attributes #

    @Attribute
    def get_lifesup_volume(self):                                           # [m^3] Volume used by life support
        life_support_volume = self.Oxygen.get_oxygen_volume + \
                              self.Water.get_system_volume + \
                              self.Food.get_farm_volume

        return life_support_volume

    @Attribute
    def get_lifesup_power(self):                                            # [W] Power used by life support
        life_support_power = self.Oxygen.get_oxygen_power + \
                             self.Water.get_system_power + \
                             self.Food.get_farm_power

        return life_support_power


if __name__ == '__main__':
    from parapy.gui import display
    obj = LifeSupport(label='Life Support')
    display(obj)
