from parapy.core import *


class Storage(Base):
    NumberOfCompartments = Input(3)                 # Number of storage compartments
    CompartmentVolume = Input(1)                    # [m^3] Volume occupied by 1 compartment

    @Attribute
    def get_storage_volume(self):
        StorageVolume = self.NumberOfCompartments * self.CompartmentVolume
        return StorageVolume


if __name__ == '__main__':
    from parapy.gui import display
    obj = Storage(label='Storage Module')
    display(obj)
