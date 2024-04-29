from parapy.core import *
from parapy.geom import *
from SciModule import Science
from CommsModule import Communications
from Storage import Storage
from RepairWorkshop import Repair
from Airlock import Airlock
from LivingQuarters import LivingQuarters
from LifeSupport import LifeSupport
import math as m
import numpy as np


class Habitat(GeomBase):                        # Consider using Geombase for building hab

    NumberOfOccupants = Input(1)                # Number of persons living in Hab
    # HabHeight = Input(20)                       # [m] Printable height of Hab
    NumberOfFloors = Input(3)                   # Number of floors in the Hab

    NumberOfScienceModules = Input(1)           # Number of Science Modules
    NumberOfWorkshops = Input(1)                # Number of Workshops
    NumberOfAirlocks = Input(1)                 # Number of Airlocks

# Maybe an input can be a choice of environment rather
# than individual environmental/atmospheric inputs

    Gravity = Input(9.81)                       # [m/s^2] Gravitational acceleration
    Radiation = Input(6.2)                      # [mSv] Average natural radiation level
    WindSpeed = Input(120)                      # [km/h] Wind speed to sustain
    AtmosphericDensity = Input(1.293)           # [kg/m^3] Atmospheric density of planet

### Modules ###

    @Part
    def ScienceModule(self):
        return Science(quantify=self.NumberOfScienceModules)

    @Part
    def Communications(self):
        return Communications()

    @Part
    def StorageModule(self):
        return Storage()

    @Part
    def RepairWorkshop(self):
        return Repair(quantify=self.NumberOfWorkshops)

    @Part
    def Airlock(self):
        return Airlock(quantify=self.NumberOfAirlocks)

    @Part
    def LivingQuarters(self):
        return LivingQuarters()

    @Part
    def LifeSupport(self):
        return LifeSupport()

### Geometry ###

    @Attribute
    def radii(self):
        x = np.linspace(4, 25, self.NumberOfFloors+2)
        y = np.zeros(len(x))
        for i in range(len(x)):
            y[i] = m.sqrt(x[i])
        return np.flip(y)

    @Part
    def hab_profiles(self):
        return Circle(quantify=self.NumberOfFloors+2,
                      radius=self.radii[child.index],
                      position=translate(self.position
                                         if child.index == 0
                                         else child.previous.position, 'z', 3))

    @Part
    def inner_shell(self):
        return LoftedSurface(profiles=self.hab_profiles)

    @Part
    def hab_floors(self):
        return CircularFace(quantify=self.NumberOfFloors+2,
                            radius=self.radii[child.index],
                            position=translate(self.position
                                               if child.index == 0
                                               else child.previous.position, 'z', 3))

    w_step = 1.5
    l_step = 0.5
    h_step = 0.5
    t_step = 0.2
    radius = 1

    @Attribute
    def angle_step(self):
        # revolutions / Height difference in step
        return (self.NumberOfFloors/3) * 2 * m.pi / (6*self.NumberOfFloors - 1)

    @Part
    def steps(self):
        return Box(quantify=6*self.NumberOfFloors - 1,
                   width=self.w_step,
                   length=self.l_step,
                   height=self.t_step,
                   position=translate(rotate(self.position.translate('z', 3)
                                             if child.index == 0
                                             else child.previous.position, 'z', self.angle_step),
                                      'z', self.h_step),
                   )

    @Part
    def inner_column(self):
        return Cylinder(radius=self.radius/2,
                        height=(self.NumberOfFloors * 3) + 3,
                        position=XOY.translate('z', 3))

### Module Attributes ###

    @Attribute
    def get_tot_use_vol(self):
        SciVol = self.ScienceModule[0].get_science_volume * self.NumberOfScienceModules
        CommsVol = self.Communications.get_comms_volume
        StorVol = self.StorageModule.get_storage_volume
        WorkVol = self.RepairWorkshop[0].WorkshopVolume
        AirVol = self.Airlock[0].get_airlock_volume
        LQVol = self.LivingQuarters.get_livquart_volume + self.LivingQuarters.BedVolume * self.NumberOfOccupants
        LSVol = self.LifeSupport.get_lifesup_volume

        TotalVolumeUsed = SciVol + CommsVol + StorVol + WorkVol + AirVol + LQVol + LSVol

        return TotalVolumeUsed                  # [m^3] Hab volume used

    @Attribute
    def get_tot_power_req(self):
        SciPow = self.ScienceModule[0].get_science_power * self.NumberOfScienceModules
        CommsPow = self.Communications.get_comms_power
        WorkPow = self.RepairWorkshop[0].WorkshopPower * self.NumberOfWorkshops
        AirPow = self.Airlock[0].AirlockPower * self.NumberOfAirlocks
        LQPow = self.LivingQuarters.get_livquart_power
        LSPow = self.LifeSupport.get_lifesup_power

        TotalPowerRequired = SciPow + CommsPow + WorkPow + AirPow + LQPow + LSPow

        return TotalPowerRequired               # [kW] Total power requirement of Hab


if __name__ == '__main__':
    from parapy.gui import display
    obj = Habitat(label='Habitat')
    display(obj)



