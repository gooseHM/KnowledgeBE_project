from parapy.core import *


class Food(Base):
    FarmLand = Input(20)                                 # [m^2] Farm land required
    UVLampPow = Input(2)                                 # [kW] Power required for 1 UV Lamp
    WaterRequired = Input(2)                             # [L/min] Water requirement for 1 m^2 of farm land

    @Attribute
    def get_UVlamps(self):
        NumberOfUVLamps = self.FarmLand/5
        return NumberOfUVLamps

    @Attribute
    def get_farm_volume(self):
        FarmVolume = self.FarmLand * 2
        return FarmVolume

    @Attribute
    def get_farm_power(self):
        FarmPower = self.get_UVlamps * self.UVLampPow
        return FarmPower

    @Attribute
    def get_water_req(self):
        FarmWaterRequired = self.FarmLand * self.WaterRequired
        return FarmWaterRequired


if __name__ == '__main__':
    from parapy.gui import display
    obj = Food(label='Food')
    display(obj)
