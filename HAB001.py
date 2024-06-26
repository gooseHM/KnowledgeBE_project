from parapy.core import *
from parapy.geom import *
from parapy.gui import display
from parapy.exchange.stl import STLWriter
from parapy.exchange.step import STEPWriter
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
import openpyxl

DIR = os.path.dirname(__file__)
os.system("taskkill /f /im excel.exe")


class Habitat(GeomBase):

    # Instantiating Excel template
    specs = openpyxl.load_workbook('Habitat_Design_Specification.xlsx')
    data = specs['Data']
    inout = specs['Design Specification']

    # Inputs:
    Body = Input(inout['K4'].value)                                 # Environment selection
    NumberOfOccupants = Input(inout['K5'].value)                    # Number of occupants
    MissionDuration = Input(inout['K6'].value)                      # Mission duration in years
    MaxPrintHeight = Input(inout['K7'].value)                       # [m] Printable height of Hab

    File_name = Input(str('Habitat_specs_Mars_01.xlsx'))
# Naming and saving Excel #
    @Attribute
    def habitat_save_file(self):
        return self.save_output

# Modules #

    @Part
    def science_module(self):
        return Science(NumberOfOccupants=self.min_occupants)

    @Part
    def communications(self):
        return Communications(NumberOfOccupants=self.min_occupants)

    @Part
    def storage_module(self):
        return Storage(NumberOfOccupants=self.min_occupants,
                       MissionDuration=self.min_stay)

    @Part
    def repair_workshop(self):
        return Repair()

    @Part
    def airlock(self):
        return Airlock()

    @Part
    def living_quarters(self):
        return LivingQuarters(NumberOfOccupants=self.min_occupants)

    @Part
    def life_support(self):
        return LifeSupport(A_vertical=self.get_lat_surf_area,
                           A_base=self.get_base_area,
                           Q_sys=self.get_tot_power_req,
                           Body=self.environment,
                           NumberOfOccupants=self.min_occupants,
                           MissionDuration=self.min_stay,
                           Q_heat=self.life_support.Heating.Q_heat)

# Geometry #

    base_radius = 5
    roof_radius = 2

    @Attribute  # Creates loft profile definitions
    def radii(self):
        x = np.linspace(self.roof_radius**2, self.base_radius**2, self.build_height + 2)
        y = np.zeros(len(x))
        for i in range(len(x)):
            y[i] = m.sqrt(x[i])
        return np.flip(y)

    @Part
    def hab_profiles(self):                                         # Creates loft profiles
        return Circle(quantify=self.build_height+2,
                      radius=self.radii[child.index],
                      position=translate(self.position
                                         if child.index == 0
                                         else child.previous.position, 'z', 3))

    @Part
    def habitat_geometry(self):                                     # Fuses airlock with main Hab body
        return FusedSolid(shape_in=FusedSolid(shape_in=Box(length=self.airlock.airlock_dims[0],
                                                           width=self.airlock.airlock_dims[1],
                                                           height=self.airlock.airlock_dims[2],
                                                           position=XOY.translate('x', -1.5, 'z', 2.5)),
                                              tool=SewnSolid(built_from=[ScaledSurface(surface_in=LoftedSurface(profiles=self.hab_profiles),
                                                                                       reference_point=Point(0, 0, 3),
                                                                                       factor=(self.life_support.Heating.t_min + 5)/5),
                                                                         Face(island=ScaledCurve(curve_in=self.hab_profiles[-1],
                                                                                                 reference_point=Point(0, 0, 3),
                                                                                                 factor=(self.life_support.Heating.t_min+5)/5)),
                                                                         Face(island=ScaledCurve(curve_in=self.hab_profiles[0],
                                                                                                 reference_point=Point(0, 0, 3),
                                                                                                 factor=(self.life_support.Heating.t_min+5)/5))])),
                          tool=Cylinder(radius=self.radii[0]*(self.life_support.Heating.t_min + 5)/5,
                                        height=0.5,
                                        position=XOY.translate('z', 2.5)))

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
    def angle_step(self):                                           # Revolutions / Height difference in step
        return (self.build_height/3) * 2 * m.pi / (6*self.build_height - 1)

    @Part
    def steps(self):                                                # Steps definitions
        return Box(quantify=6*self.build_height - 1,
                   width=self.w_step,
                   length=self.l_step,
                   height=self.t_step,
                   position=translate(rotate(self.position.translate('z', 3)
                                             if child.index == 0
                                             else child.previous.position, 'z', self.angle_step),
                                      'z', self.h_step))

    @Part
    def inner_column(self):
        return Cylinder(radius=self.radius/2,
                        height=(self.build_height * 3) + 3,
                        position=XOY.translate('z', 3))

# Habitat Attributes #

    @Attribute
    def get_available_vol(self):                                    # Available volume that can be used
        hab_vol = 0.
        for i in range(len(self.radii)-1):
            hab_vol = hab_vol + (1/3) * m.pi * 3 * \
                      (self.radii[i+1]**2 + self.radii[i+1] * self.radii[i] + self.radii[i]**2)
        return hab_vol

    @Attribute
    def get_lat_surf_area(self):                                    # Surface area of the Hab
        lat_surf_area = m.pi * self.radii[-1] ** 2
        for i in range(len(self.radii)-1):
            s = m.sqrt((self.radii[i] - self.radii[i+1])**2 + 3**2)
            lat_surf_area = lat_surf_area + m.pi * (self.radii[i] + self.radii[i+1])*s
        return lat_surf_area

    @Attribute                                                      # Area of the Hab base
    def get_base_area(self):
        base_area = m.pi * self.radii[0] ** 2
        return base_area

    @Attribute
    def get_tot_use_vol(self):                                      # Total volume used by modules
        total_used_volume = self.science_module.get_science_volume + \
                            self.communications.get_comms_volume + \
                            self.storage_module.get_storage_volume + \
                            self.repair_workshop.get_workshop_volume + \
                            self.airlock.get_airlock_volume + \
                            self.living_quarters.get_livquart_volume + \
                            self.life_support.get_lifesup_volume

        return total_used_volume

    @Attribute
    def get_tot_power_req(self):                                    # Total power used by modules
        total_required_power = self.science_module.get_science_power + \
                               self.communications.get_comms_power + \
                               self.repair_workshop.get_workshop_power + \
                               self.airlock.get_airlock_power + \
                               self.living_quarters.get_livquart_power + \
                               self.life_support.get_lifesup_power

        return total_required_power

    @Attribute                                                      # Habitat floor count determination logic
    def build_height(self):
        start = 0
        mode = True
        while mode:
            x = np.linspace(self.roof_radius**2, self.base_radius**2, start + 2)
            y = np.zeros(len(x))
            for k in range(len(x)):
                y[k] = m.sqrt(x[k])
            z = np.flip(y)

            available_vol = 0.
            for p in range(len(z) - 1):
                available_vol = available_vol + (1 / 3) * m.pi * 3 * \
                          (z[p + 1] ** 2 + z[p + 1] * z[p] + z[p] ** 2)

            if self.get_tot_use_vol > available_vol and (start * 3) + 3 <= self.print_height:
                start += 1
            else:
                if (start * 3) + 3 > self.print_height:
                    start -= 1
                    height_error = f"Current configuration exceeds maximum build volume."
                    warnings.warn(height_error)
                    generate_warning("Warning: Build Height", height_error)
                mode = False
        return start

    @Attribute
    def print_volume(self):
        return self.habitat_geometry.volume - self.get_available_vol

    @Attribute
    def hab_height(self):
        return self.build_height*3 + 3

# STL Output #

    @Part
    def protective_shell_stl(self):
        return STLWriter(shape_in=[self.habitat_geometry],
                         default_directory=DIR)

# STEP Output #

    @Part
    def protective_shell_step(self):
        return STEPWriter(nodes=[self.habitat_geometry],
                          default_directory=DIR)

# Output Saving to excel#
    @Attribute
    def save_output(self):
        # Geometric outputs
        self.inout['B5'] = self.life_support.Heating.t_min
        self.inout['B6'] = self.build_height
        self.inout['B7'] = self.hab_height
        self.inout['B8'] = self.base_radius
        self.inout['B9'] = self.roof_radius
        self.inout['B10'] = self.print_volume
        # Power outputs
        x = 0.001  # change to kilo Watt for output file
        self.inout['B13'] = x * self.science_module.get_science_power
        self.inout['B14'] = x * self.communications.get_comms_power
        self.inout['B16'] = x * self.repair_workshop.get_workshop_power
        self.inout['B17'] = x * self.airlock.get_airlock_power
        self.inout['B18'] = x * self.living_quarters.get_livquart_power
        self.inout['B19'] = x * self.life_support.get_lifesup_power
        self.inout['B21'] = x * self.life_support.Heating.Q_heat
        # Volume outputs
        self.inout['B24'] = self.science_module.get_science_volume
        self.inout['B25'] = self.communications.get_comms_volume
        self.inout['B26'] = self.storage_module.get_storage_volume
        self.inout['B27'] = self.repair_workshop.get_workshop_volume
        self.inout['B28'] = self.airlock.get_airlock_volume
        self.inout['B29'] = self.living_quarters.get_livquart_volume
        self.inout['B30'] = self.life_support.get_lifesup_volume

        # Out of scope design outputs
        self.inout['F6'] = self.life_support.Power.get_power_generation[0]
        self.inout['F7'] = self.life_support.Power.get_power_generation[1]

        # Life support sub outputs
        self.inout['F13'] = x*self.life_support.Oxygen.get_oxygen_power
        self.inout['F14'] = x*self.life_support.Water.get_system_power
        self.inout['F15'] = x*self.life_support.Food.get_farm_power

        self.inout['F17'] = self.life_support.Oxygen.get_oxygen_volume
        self.inout['F18'] = self.life_support.Water.get_system_volume
        self.inout['F19'] = self.life_support.Food.get_farm_volume

        # Input overwrite
        self.inout['K4'] = self.Body
        self.inout['K5'] = self.NumberOfOccupants
        self.inout['K6'] = self.MissionDuration
        self.inout['K7'] = self.MaxPrintHeight

        return self.specs.save(self.File_name)

# Error Management #

    @Attribute
    def min_occupants(self):
        if self.NumberOfOccupants < 1:
            min_person = "Number of occupants must be at least 1" \
                         "\nNumber of occupants set to 1"
            warnings.warn(min_person)
            generate_warning("Warning: Value changed", min_person)
            return 1
        elif self.NumberOfOccupants % 1 != 0:
            is_decimal = "Number of occupants must be a whole number" \
                         f"\nNumber of occupants set to {round(self.NumberOfOccupants)}"
            warnings.warn(is_decimal)
            generate_warning("Warning: Value changed", is_decimal)
            return round(self.NumberOfOccupants)
        else:
            return self.NumberOfOccupants

    @Attribute
    def min_stay(self):
        if self.MissionDuration < 0.5:
            min_stay = "Non feasible mission duration" \
                        "\nMission duration set to 0.5 years"
            warnings.warn(min_stay)
            generate_warning("Warning: Value changed", min_stay)
            return 0.5
        else:
            return self.MissionDuration

    @Attribute
    def print_height(self):
        if self.MaxPrintHeight < 3:
            min_stay = "Print height is too low" \
                        "\nPrint height set to 3m"
            warnings.warn(min_stay)
            generate_warning("Warning: Value changed", min_stay)
            return 3
        else:
            return self.MaxPrintHeight

    @Attribute
    def environment(self):
        if self.Body != "Mars" and self.Body != "Moon":
            type_error = "Unavailable Celestial Body" \
                         "\n try 'Moon' or 'Mars'"
            warnings.warn(type_error)
            generate_warning("Warning: Incorrect Input", type_error)
            return "'Mars'"
        else:
            return self.Body


def generate_warning(warning_header, msg):
    from tkinter import Tk, messagebox

    window = Tk()
    window.withdraw()

    messagebox.showwarning(warning_header, msg)


if __name__ == '__main__':
    obj = Habitat(label='Habitat')
    display(obj)
