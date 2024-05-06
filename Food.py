from parapy.core import *


class Food(Base):

    NumberOfOccupants = Input(1)
    MissionDuration = Input(1)

    FarmLand = Input(180)                                # [m^2] Farm land required for 1 person for 1 year
    UVLampPow = Input(500)                               # [W] Power required for 1 UV Lamp
    # WaterRequired = Input(2)                             # [L/min] Water requirement for 1 m^2 of farm land

    @Attribute
    def get_uvlamps(self):
        NumberOfUVLamps = self.FarmLand/5
        return NumberOfUVLamps

    @Attribute
    def get_farm_volume(self):
        farm_volume = self.FarmLand * self.NumberOfOccupants
        return farm_volume

    @Attribute
    def get_farm_power(self):
        farm_power = self.get_uvlamps * self.UVLampPow
        return farm_power

    # @Attribute
    # def get_water_req(self):
    #     FarmWaterRequired = self.FarmLand * self.WaterRequired
    #     return FarmWaterRequired


if __name__ == '__main__':
    from parapy.gui import display
    obj = Food(label='Food')
    display(obj)
