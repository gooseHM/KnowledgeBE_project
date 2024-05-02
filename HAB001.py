from parapy.core import *
from parapy.geom import *
from parapy.exchange.stl import STLWriter
from SciModule import Science
from CommsModule import Communications
from Storage import Storage
from RepairWorkshop import Repair
from Airlock import Airlock
from LivingQuarters import LivingQuarters
from LifeSupport import LifeSupport
import math as m
import numpy as np
import warnings
import os

DIR = os.path.dirname(__file__)


class Habitat(GeomBase):
    ''' Habitat class
    todo add base geometry
     for presentation purpose make sure only relevant geo is displayed '''
    NumberOfOccupants = Input(1)                                            # Number of persons living in Hab
    MaxPrintHeight = Input(20.)                                             # [m] Printable height of Hab
    NumberOfFloors = Input(3)                                               # Number of floors in the Hab

    NumberOfWorkshops = Input(1)                                            # Number of Workshops
    NumberOfAirlocks = Input(1)                                             # Number of Airlocks

# Maybe an input can be a choice of environment rather
# than individual environmental/atmospheric inputs

    Gravity = Input(9.81)                                                   # [m/s^2] Gravitational acceleration
    Radiation = Input(6.2)                                                  # [mSv] Average natural radiation level
    WindSpeed = Input(120)                                                  # [km/h] Wind speed to sustain
    AtmosphericDensity = Input(1.293)                                       # [kg/m^3] Atmospheric density of planet


# Modules #

    @Part
    def science_module(self):
        return Science(pass_down="NumberOfOccupants")

    @Part
    def communications(self):
        return Communications()

    @Part
    def storage_module(self):
        return Storage()

    @Part
    def repair_workshop(self):
        return Repair(quantify=self.NumberOfWorkshops)

    @Part
    def airlock(self):
        return Airlock()

    @Part
    def living_quarters(self):
        return LivingQuarters(pass_down="NumberOfOccupants")

    @Part
    def life_support(self):
        return LifeSupport(A_vertical=self.get_lat_surf_area, A_base=self.get_base_area,
                           Q_sys=self.get_tot_power_req)

# Geometry #

    @Attribute                                                      # Create loft profiles for inner shell
    def radii(self):
        x = np.linspace(4, 25, self.build_height+2)
        y = np.zeros(len(x))
        for i in range(len(x)):
            y[i] = m.sqrt(x[i])
        return np.flip(y)

    @Part
    def hab_profiles(self):
        return Circle(quantify=self.build_height+2,
                      radius=self.radii[child.index],
                      position=translate(self.position
                                         if child.index == 0
                                         else child.previous.position, 'z', 3))

    @Part
    def inner_shell(self):
        return LoftedSurface(profiles=self.hab_profiles)

    @Part
    def inner_volume(self):
        return SewnSolid(built_from=[self.inner_shell, self.hab_floors[0], self.hab_floors[-1]])

    # @Part
    # def test_circle(self):
    #     return Circle(radius=5+self.HabThickness, position=XOY.translate('z', 3))

    @Part
    def outer_shell(self):
        return ScaledSurface(surface_in=self.inner_shell,
                             reference_point=Point(0, 0, 3),
                             factor=(self.life_support.Heating.t_min + 5)/5)

    @Attribute
    def outer_floor_profile(self):
        return ScaledCurve(curve_in=self.hab_profiles[0],
                           reference_point=Point(0, 0, 3),
                           factor=(self.life_support.Heating.t_min+5)/5)

    @Attribute
    def outer_roof_profile(self):
        return ScaledCurve(curve_in=self.hab_profiles[-1],
                           reference_point=Point(0, 0, 3),
                           factor=(self.life_support.Heating.t_min+5)/5)

    @Part
    def outer_floor(self):
        return Face(island=self.outer_floor_profile)

    @Part
    def outer_roof(self):
        return Face(island=self.outer_roof_profile)

    @Part
    def main_hab(self):
        return SewnSolid(built_from=[self.outer_shell, self.outer_floor, self.outer_roof])

    @Part
    def airlock_body(self):
        return Box(length=self.airlock.airlock_dims[0],
                   width=self.airlock.airlock_dims[1],
                   height=self.airlock.airlock_dims[2],
                   position=XOY.translate('x', -1.5, 'z', 3))

    @Part
    def filleted_airlock(self):
        return FilletedSolid(built_from=self.airlock_body,
                             radius=0.5,
                             edge_table=self.airlock_body.top_face.edges)

    @Part
    def printed_shell(self):
        return FusedSolid(shape_in=self.filleted_airlock, tool=self.main_hab)

    # @Part
    # def printed_shell(self):
    #     return SubtractedSolid(shape_in=self.full_hab, tool=self.inner_volume)

    @Part
    def hab_floors(self):
        return CircularFace(quantify=self.build_height+2,
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
        return (self.build_height/3) * 2 * m.pi / (6*self.build_height - 1)

    @Part
    def steps(self):
        return Box(quantify=6*self.build_height - 1,
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
                        height=(self.build_height * 3) + 3,
                        position=XOY.translate('z', 3))

# Habitat Attributes #

    @Attribute
    def get_available_vol(self):
        hab_vol = 0.
        for i in range(len(self.radii)-1):
            hab_vol = hab_vol + (1/3) * m.pi * 3 * \
                      (self.radii[i+1]**2 + self.radii[i+1] * self.radii[i] + self.radii[i]**2)
        return hab_vol

    @Attribute
    def get_lat_surf_area(self):
        lat_surf_area = m.pi * self.radii[-1] ** 2
        for i in range(len(self.radii)-1):
            s = m.sqrt((self.radii[i] - self.radii[i+1])**2 + 3**2)
            lat_surf_area = lat_surf_area + m.pi * (self.radii[i] + self.radii[i+1])*s
        return lat_surf_area

    @Attribute
    def get_base_area(self):
        base_area = m.pi * self.radii[0] ** 2
        return base_area

    @Attribute
    def get_tot_use_vol(self):
        storage_volume = self.storage_module.get_storage_volume
        workshop_volume = self.repair_workshop[0].WorkshopVolume
        airlock_volume = self.airlock.get_airlock_volume
        life_support_volume = self.life_support.get_lifesup_volume

        total_used_volume = self.science_module.get_science_volume + self.communications.get_comms_volume + storage_volume + workshop_volume + airlock_volume + \
                            self.living_quarters.get_livquart_volume + life_support_volume

        return total_used_volume                                            # [m^3] Hab volume used

    @Attribute
    def get_tot_power_req(self):
        workshop_power = self.repair_workshop[0].WorkshopPower * self.NumberOfWorkshops
        #airlock_power = self.airlock.AirlockPower * self.NumberOfAirlocks airlock_power +
        life_support_power = self.life_support.get_lifesup_power

        total_required_power = self.science_module.get_science_power + self.communications.get_comms_power + workshop_power +  \
                               self.living_quarters.get_livquart_power + life_support_power

        return total_required_power                                         # [kW] Total power requirement of Hab

    @Attribute                                                              # Minimum/Maximum floor count errors
    def build_height(self):
        if self.NumberOfFloors*3 > self.MaxPrintHeight:
            height_error = f"Current floor count exceeds maximum print height of {self.MaxPrintHeight}m." \
                  f"\nFloor count will be set to maximum possible: {m.floor(self.MaxPrintHeight/3)} floors."
            warnings.warn(height_error)
            generate_warning("Warning: Value changed", height_error)
            return m.floor(self.MaxPrintHeight/3)
        elif self.NumberOfFloors <= 1:
            height_error2 = f"Current floor count is not enough to house all modules" \
                            f"\nFloor count set to minimum possible: ({2})"
            warnings.warn(height_error2)
            generate_warning("Warning: Value changed", height_error2)
            return 2
        else:
            return self.NumberOfFloors

# STL Output #

    @Part
    def protective_shell(self):
        return STLWriter(shape_in=[self.printed_shell],
                         default_directory=DIR)


def generate_warning(warning_header, msg):
    from tkinter import Tk, messagebox

    window = Tk()
    window.withdraw()

    messagebox.showwarning(warning_header, msg)


if __name__ == '__main__':
    from parapy.gui import display
    obj = Habitat(label='Habitat')
    display(obj)
