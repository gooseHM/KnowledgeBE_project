from parapy.core import *
#from Temp_calc_module import Thermal

class rr(Base):

    HeatingPower = Thermal.Q_heat                           # [kW] Heating power input
    StorageCapacity = Input(5)                           # [kW] Heating power output


if __name__ == '__main__':
    from parapy.gui import display
    obj = Heating(label='Heating')
    display(obj)
