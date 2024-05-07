from parapy.core import *
import numpy as np


class Water(Base):

    NumberOfOccupants = Input(1)
    MissionDuration = Input(1)
    FarmVolume = Input(180)                                             # [m^3] Farmland requiring irrigation

    @Attribute
    def water_recovery_system(self):
        wrs_volume = 2 * 1 * 1
        wrs_power = 350
        return wrs_volume, wrs_power

    @Attribute
    def urine_recovery_system(self):
        urs_volume = 2 * 1 * 1
        urs_power = 350
        return urs_volume, urs_power

    @Attribute
    def get_system_volume(self):
        if self.MissionDuration > 1:
            return self.water_recovery_system[0] * \
               np.ceil(self.NumberOfOccupants/5) * \
               np.ceil(self.FarmVolume/500) + \
               self.urine_recovery_system[0] * \
               np.ceil(self.NumberOfOccupants/5)
        else:
            return self.water_recovery_system[0] * \
               np.ceil(self.NumberOfOccupants/5) + \
               self.urine_recovery_system[0] * \
               np.ceil(self.NumberOfOccupants/5)

    @Attribute
    def get_system_power(self):
        if self.MissionDuration > 1:
            return self.water_recovery_system[1] * \
               np.ceil(self.NumberOfOccupants/5) * \
               np.ceil(self.FarmVolume/500) + \
               self.urine_recovery_system[1] * \
               np.ceil(self.NumberOfOccupants/5)
        else:
            return self.water_recovery_system[1] * \
               np.ceil(self.NumberOfOccupants/5) + \
               self.urine_recovery_system[1] * \
               np.ceil(self.NumberOfOccupants/5)


if __name__ == '__main__':
    from parapy.gui import display
    obj = Water(label='Water')
    display(obj)
