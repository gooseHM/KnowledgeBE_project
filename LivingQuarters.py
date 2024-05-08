from parapy.core import *


class LivingQuarters(Base):

    NumberOfOccupants = Input(1)

    ExerciseMachineVolume = 3                       # [m^3] Exercise Machine Volume (treadmill)
    LavatoryVolume = 2                              # [m^3] Lavatory Volume
    ExerciseMachinePower = 1500                     # [W] Exercise Machine Power Requirement (treadmill)
    BedVolume = 2                                   # [m^3] Bed Volume
    LivingSpace = 20                                # [m^3] Living space to walk around

    @Attribute
    def get_livquart_volume(self):
        lq_vol = (self.NumberOfOccupants * self.BedVolume) + \
                 self.ExerciseMachineVolume + self.LavatoryVolume + \
                 self.LivingSpace
        return lq_vol

    @Attribute
    def get_livquart_power(self):
        lq_power = self.ExerciseMachinePower
        return lq_power


if __name__ == '__main__':
    from parapy.gui import display
    obj = LivingQuarters(label='Living Quarters')
    display(obj)
