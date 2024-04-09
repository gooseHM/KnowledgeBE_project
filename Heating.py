from parapy.core import *


class Heating(Base):
    HeatingPower = Input(10)                             # [kW] Heating power input
    StorageCapacity = Input(5)                           # [kW] Heating power output


if __name__ == '__main__':
    from parapy.gui import display
    obj = Heating(label='Heating')
    display(obj)
