from parapy.core import *
from SciModule import Science
from CommsModule import Communications
from Storage import Storage
from RepairWorkshop import Repair
from Airlock import Airlock
from LivingQuarters import LivingQuarters
from LifeSupport import LifeSupport


class Habitat(Base):                            # Consider using Geombase for building hab

    NumberOfOccupants = Input(1)                # Number of persons living in Hab
    HabHeight = Input(20)                       # [m] Printable height of Hab

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

### Attributes ###

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



