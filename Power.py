from parapy.core import *


class Power(Base):
    PowerGenerated = Input(1)                            # [kW] Power generated
    StorageCapacity = Input(10)                          # [kJ] Energy Storage Capacity


if __name__ == '__main__':
    from parapy.gui import display
    obj = Power(label='Power')
    display(obj)
