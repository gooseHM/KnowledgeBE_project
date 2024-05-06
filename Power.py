from parapy.core import *


class Power(Base):

    Q_sys = Input()                                             # [W] Total power consumed by habitat
    s_panel = 700                                               # [W] Solar output of a 2x2 m^2 solar panel

    @Attribute
    def get_power_generation(self):
        if self.Q_sys <= 50000:
            NumberOfSolarPanels = round(self.Q_sys / self.s_panel) + 5
            NumberOfNuclearReactors = 0
            return NumberOfSolarPanels, NumberOfNuclearReactors
        else:
            NumberOfSolarPanels = 80
            NumberOfNuclearReactors = round((self.Q_sys - 45000) / 5000)
            return NumberOfSolarPanels, NumberOfNuclearReactors


if __name__ == '__main__':
    from parapy.gui import display
    obj = Power(label='Power')
    display(obj)
