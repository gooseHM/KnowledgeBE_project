from parapy.core import *


class Food(Base):

    NumberOfOccupants = Input(1)
    MissionDuration = Input(1)

    FarmLand = Input(180)                                # [m^2] Farm land required for 1 person for 1 year
    UVLampPow = Input(500)                               # [W] Power required for 1 UV Lamp

    @Attribute
    def get_uvlamps(self):
        uv_lamps = self.FarmLand/5
        return uv_lamps

    @Attribute
    def get_farm_volume(self):
        if self.MissionDuration > 1:
            farm_volume = self.FarmLand * self.NumberOfOccupants
            return farm_volume
        else:
            return 0

    @Attribute
    def get_farm_power(self):
        if self.MissionDuration > 1:
            farm_power = self.get_uvlamps * self.UVLampPow
            return farm_power
        else:
            return 0


if __name__ == '__main__':
    from parapy.gui import display
    obj = Food(label='Food')
    display(obj)
