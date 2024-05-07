from parapy.core import *


class Storage(Base):

    NumberOfOccupants = Input(1)
    MissionDuration = Input(1)
    GeneralStorage = Input(10)

    @Attribute
    def food_storage(self):                         # [m^3] Volume required to store a year's worth of rations
        food_storage_volume = 35 * self.NumberOfOccupants * self.MissionDuration
        return food_storage_volume

    @Attribute
    def personal_storage(self):                     # 1m^3 Box per person for personal storage
        personal_volume = self.NumberOfOccupants
        return personal_volume

    @Attribute
    def get_storage_volume(self):
        if self.MissionDuration <= 1:
            storage_volume = self.food_storage + self.personal_storage + self.GeneralStorage
            return storage_volume
        else:
            storage_volume = self.personal_storage + self.GeneralStorage
            return storage_volume


if __name__ == '__main__':
    from parapy.gui import display
    obj = Storage(label='Storage Module')
    display(obj)
