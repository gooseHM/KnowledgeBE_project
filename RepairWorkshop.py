from parapy.core import *


class Repair(Base):
    WorkshopVolume = Input(1)                            # [m^3] Volume occupied by repair workshop
    WorkshopPower = Input(10)                            # [kW] Power consumption of repair workshop


if __name__ == '__main__':
    from parapy.gui import display
    obj = Repair(label='Repair Workshop')
    display(obj)
