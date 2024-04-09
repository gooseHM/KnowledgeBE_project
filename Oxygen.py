from parapy.core import *


class Oxygen(Base):
    OxygenSysPower = Input(10)                           # [kW] Oxygen system power required
    OxygenSupply = Input(15)                             # [L/hr] Oxygen output


if __name__ == '__main__':
    from parapy.gui import display
    obj = Oxygen(label='Oxygen')
    display(obj)
