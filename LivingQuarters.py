from parapy.core import *


class LivingQuarters(Base):
    NumberOfExerciseMachines = Input(1)             # Number of exercise equipment
    NumberOfLavatories = Input(1)                   # Number of lavatories
    ExerciseMachineVolume = Input(1)                # [m^3] Volume of one exercise machine
    LavatoryVolume = Input(5)                       # [m^3] Volume of one lavatory
    ExerciseMachinePower = Input(10)                # [kW] Power required for one exercise machine
    LavatoryPower = Input(5)                        # [kW] Power required for one lavatory
    BedVolume = Input(5)                            # [m^3] Volume of 1 bed

    @Attribute
    def get_livquart_volume(self):
        LQVolume = self.NumberOfExerciseMachines * self.ExerciseMachineVolume + \
                   self.NumberOfLavatories * self.LavatoryVolume
        return LQVolume

    @Attribute
    def get_livquart_power(self):
        LQPower = self.NumberOfExerciseMachines * self.ExerciseMachinePower + \
                  self.NumberOfLavatories + self.LavatoryPower
        return LQPower


if __name__ == '__main__':
    from parapy.gui import display
    obj = LivingQuarters(label='Living Quarters')
    display(obj)
