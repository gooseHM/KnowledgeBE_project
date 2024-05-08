import numpy as np
from parapy.core import *


import matlab
import matlab.engine
from Matlab_files import me
import openpyxl
class Heating(Base):
    '''Define relevant properties for thermal model.
    Provides minimum thickness based on the inputs below.

    It is possible to change the % of the system power
    that is allowed for the maximum heating. And
     the percentage of system power that turns into heat.
      [Q_max & perc_Qsys] respectively (In GUI) '''
    me.addpath('Matlab_files')

    specs = openpyxl.load_workbook('Habitat_Design_Specification.xlsx')
    data = specs['Data']
    inout = specs['Design Specification']
    #Inputs:
    Body = Input()
    # Temperatures
    T_inside = Input(20)                            # Temperature inside the habitat

    # Geometry
    A_base = Input(50)                              # Base Area in m2
    A_vertical = Input(560)                         # Outer wall Area in m2
    t_base = Input(0.25)                            # Foundation/Base Thickness in m

    # Power
    Q_sys = Input(25000)                            # Nominal Power use in W
    Q_max = Input(0.05)                             # Percentage of system power allowed to be used as heater
    perc_Qsys = Input(0.10)                         # Percentage of system power that turns into heat

    @Attribute
    def get_R_info(self):
        #Returns the regolith properties for the body the habitat is designed for
        b = self.Body
        specs = openpyxl.load_workbook('Habitat_Design_Specification.xlsx')
        Bi = specs['Data']

        if b == 'Mars':
            c = 'B'
        elif b == 'Moon':
            c = 'C'
        else:
            c = 'G'

        R_c = Bi[c + str(7)].value
        R_e = Bi[c + str(8)].value
        T_min = Bi[c + str(5)].value  #Coldest temp on body
        return R_c, R_e, T_min

    @Attribute
    def Thermal_model(self):
        # Runs the MATLAB models and provides the inputs for the models
        input = matlab.double([self.get_R_info[0],self.get_R_info[1],
                               self.T_inside,self.get_R_info[2],
                               self.A_base,self.A_vertical,self.t_base,
                               self.Q_sys,self.Q_max,self.perc_Qsys])

        x = me.Thermal_sizing(input,nargout=1)               # Output is changed to an array and found in the Attributes
        return np.array(x)
    @Attribute
    def Q_heat(self):
        # Heating power output
        Q_heat = self.Thermal_model[0][0]
        return Q_heat
    @Attribute
    def t_min(self):
        # Minimum thickness for isolation
        t_min = self.Thermal_model[0][1]
        return t_min
