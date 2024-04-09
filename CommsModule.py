from parapy.core import *


class Communications(Base):
    NumberOfCommunicationDevices = Input(3)          # Number of comms devices
    CommsVolume = Input(1)                            # [m^3] Volume occupied by 1 comms equipment
    CommsPower = Input(10)                            # [kW] Power consumption of 1 comms equipment

    @Attribute
    def get_comms_volume(self):
        CommsVolume = self.NumberOfCommunicationDevices * self.CommsVolume
        return CommsVolume

    @Attribute
    def get_comms_power(self):
        CommsPower = self.NumberOfCommunicationDevices * self.CommsPower
        return CommsPower


if __name__ == '__main__':
    from parapy.gui import display
    obj = Communications(label='Communications')
    display(obj)