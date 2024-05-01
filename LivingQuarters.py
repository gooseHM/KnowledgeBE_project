from parapy.core import *
import warnings

class LivingQuarters(Base):
    NumberOfOccupants = Input(1)                    # Number of occupants

    ExerciseMachineVolume = 3                       # [m^3] Exercise Machine Volume (treadmill)
    LavatoryVolume = 2                              # [m^3] Lavatory Volume
    ExerciseMachinePower = 1500                     # [W] Exercise Machine Power Requirement (treadmill)
    BedVolume = 2                                   # [m^3] Bed Volume

    @Attribute
    def get_livquart_volume(self):
        lq_vol = (self.min_occupants * self.BedVolume) + self.ExerciseMachineVolume + self.LavatoryVolume
        return lq_vol

    @Attribute
    def get_livquart_power(self):
        lq_power = self.ExerciseMachinePower
        return lq_power

    @Attribute
    def min_occupants(self):
        if self.NumberOfOccupants < 1:
            min_person = "Number of occupants must be at least 1" \
                         "\nNumber of occupants set to 1"
            warnings.warn(min_person)
            generate_warning("Warning: Value changed", min_person)
            return 1
        else:
            return self.NumberOfOccupants


def generate_warning(warning_header, msg):
    from tkinter import Tk, messagebox

    window = Tk()
    window.withdraw()

    messagebox.showwarning(warning_header, msg)


if __name__ == '__main__':
    from parapy.gui import display
    obj = LivingQuarters(label='Living Quarters')
    display(obj)
