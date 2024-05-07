from parapy.core import *


class Science(Base):

    NumberOfOccupants = Input(1)

    @Attribute
    def human_research_lab(self):
        hrl_volume = 8                              # [m^3] Volume required for HRM lab
        hrl_power = 5000                            # [W] Power required for HRM lab
        return hrl_volume, hrl_power

    @Attribute
    def biology_lab(self):
        bio_volume = 10                             # [m^3] Volume required for Bio lab
        bio_power = 7500                            # [W] Power required for Bio lab
        return bio_volume, bio_power

    @Attribute
    def physics_lab(self):
        phy_volume = 16                             # [m^3] Volume required for Bio lab
        phy_power = 2000                            # [W] Power required for Phy lab
        return phy_volume, phy_power

    @Attribute
    def geology_lab(self):
        geo_volume = 2                              # [m^3] Volume required for Bio lab
        geo_power = 500                             # [W] Power required for Geo lab
        return geo_volume, geo_power

    @Attribute
    def get_science_volume(self):
        if self.NumberOfOccupants < 3:
            science_volume = self.human_research_lab[0] + self.biology_lab[0]
            return science_volume
        else:
            science_volume = self.human_research_lab[0] + self.biology_lab[0] + \
                            self.physics_lab[0] + self.geology_lab[0]
            return science_volume

    @Attribute
    def get_science_power(self):
        if self.NumberOfOccupants < 3:
            science_power = self.human_research_lab[1] + self.biology_lab[1]
            return science_power
        else:
            science_power = self.human_research_lab[1] + self.biology_lab[1] + \
                            self.physics_lab[1] + self.geology_lab[1]
            return science_power


if __name__ == '__main__':
    from parapy.gui import display
    obj = Science(label='Science Module')
    display(obj)
