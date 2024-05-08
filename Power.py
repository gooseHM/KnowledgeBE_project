from parapy.core import *
import openpyxl

class Power(Base):
    Body =Input()
    Q_sys = Input()                                             # [W] Total power consumed by habitat
    Q_heat = Input()
    s_panel = 700                                               # [W] Solar output of a 2x2 m^2 solar panel on Mars

    @Attribute
    def get_solar_flux_ratio(self):
        # Returns the regolith properties for the body the habitat is designed for
        b = self.Body
        specs = openpyxl.load_workbook('Habitat_Design_Specification.xlsx')
        Bi = specs['Data']

        if b == 'Mars':
            c = 'B'
        elif b == 'Moon':
            c = 'C'
        else:
            c = 'G'

        solar_flux = Bi[c + str(10)].value
        solar_flux_ratio = solar_flux / Bi['B10'].value
        return solar_flux_ratio
    @Attribute
    def get_power_generation(self):
        Q_sys = self.Q_sys + self.Q_heat
        if self.Q_sys <= 50000:
            solar_panels = round(Q_sys/ self.s_panel/self.get_solar_flux_ratio ) + 5
            nuclear_reactors = 0
            return solar_panels, nuclear_reactors
        else:
            solar_panels = 80
            nuclear_reactors = round((self.Q_sys - 45000) / 5000)
            return solar_panels, nuclear_reactors


if __name__ == '__main__':
    from parapy.gui import display
    obj = Power(label='Power')
    display(obj)
