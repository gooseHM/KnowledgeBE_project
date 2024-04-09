from parapy.core import *


class Science(Base):
    NumberOfLabs = Input(3)                         # Number of lab equipment required
    LabVolume = Input(1)                            # [m^3] Volume occupied by 1 lab equipment
    LabPower = Input(10)                            # [kW] Power consumption of 1 lab equipment

    @Attribute
    def get_science_volume(self):
        ScienceVolume = self.NumberOfLabs * self.LabVolume
        return ScienceVolume

    @Attribute
    def get_science_power(self):
        SciencePower = self.NumberOfLabs * self.LabPower
        return SciencePower


if __name__ == '__main__':
    from parapy.gui import display
    obj = Science(label='Science Module')
    display(obj)
