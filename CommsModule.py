from parapy.core import *


class Communications(Base):

    NumberOfOccupants = Input(1)

    @Attribute
    def personal_comms(self):
        pers_volume = 2                             # [m^3] Volume required for personal comms
        pers_power = 100                            # [W] Power required for personal comms
        return pers_volume, pers_power

    @Attribute
    def comms_hub(self):
        hub_volume = 4                              # [m^3] Volume required for comms hub
        hub_power = 1000                            # [W] Power required for comms hub
        return hub_volume, hub_power


    @Attribute
    def get_comms_volume(self):
        CommsVolume = (self.NumberOfOccupants * self.personal_comms[0]) + self.comms_hub[0]
        return CommsVolume

    @Attribute
    def get_comms_power(self):
        CommsPower = (self.NumberOfOccupants * self.personal_comms[1]) + self.comms_hub[1]
        return CommsPower

    @Attribute
    def min_occupants(self):
        if self.NumberOfOccupants < 1:
            return 1
        else:
            return self.NumberOfOccupants


if __name__ == '__main__':
    from parapy.gui import display
    obj = Communications(label='Communications')
    display(obj)