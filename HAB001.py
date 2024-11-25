from typing import Union, Any
from parapy.core import *
from parapy.geom import *
# from parapy.gui import display
from parapy.webgui.core import Component, NodeType, get_assets_dir, get_asset_url
from parapy.webgui.app_bar import AppBar
from parapy.webgui.html import *
from parapy.webgui import mui, layout, viewer, html, plotly
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
    Body = Input('Mars')                                                # Environment selection
    NumberOfOccupants = Input(1)                                        # Number of occupants
    MissionDuration = Input(1)                                          # Mission duration in years
    MaxPrintHeight = Input(21)                                          # [m] Printable height of Hab
    DepoRate = Input(750)                                               # Regolith Deposition Rate [kg/hr]

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
        return FusedSolid(shape_in=RotatedShape(shape_in=FusedSolid(shape_in=Box(length=self.airlock.airlock_dims[0],
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
                                rotation_point=Point(0, 0, 0),
                                vector=Vector(0, 0, 1),
                                angle=m.radians(180)),

                              tool=Cylinder(radius=self.radii[0]*(self.life_support.Heating.t_min + 5)/5,
                                            height=0.5,
                                            position=XOY.translate('z', 2.5))
                            )

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

### webGUI Development ###

CustomHab = Habitat()
class Habitect(Component):
    def render(self) -> NodeType:
        return layout.AppbarWithSidebar(
            #theme={
            #    'palette': {
            #        'primary': {'main': '#d9a975'},
            #        'background': {'main': '#eed', 'sidebar': '#d9a975'},
            #        'action': {'selected': '#aa9a', 'hover': '#ccb'},
            #    }
            #},
            title="Extraterrestrial Habitat Configurator",
            logo_src=get_asset_url("habitect-high-resolution-logo-transparent.png"),
            app_bar_content=layout.Box(h_align='right',
                                       v_align='center',
                                       height='100%'),
        tabs = [
            {
                "label": "Home",
                "icon": mui.Icon['home'],
                "content": layout.Split(height='100%', weights=[0, 0, 1])[
                                InputsPanel,
                                mui.Divider(orientation='vertical'),
                                viewer.Viewer(objects=CustomHab),
                ],
            },
            {
                "label": "Overview",
                "icon": mui.Icon['assessment'],
                "content": layout.Split(height='100%', weights=[1, 0, 0])[
                                Piecharts,
                                mui.Divider(orientation='vertical'),
                                OutputDialogs
                ]
            }
        ]
        )

class InputsPanel(Component):
    def render(self) -> NodeType:
        return layout.Box(orientation='vertical',
                          gap='1em',
                          style={'padding': '1em'})[
            html.code['Environment'],
                layout.SlotRadioButtons(CustomHab, 'Body', options=['Moon', 'Mars']),

            mui.FormGroup[
                mui.FormLabel["Number of Occupants"],
                mui.Slider(min=1,
                           max=5,
                           valueLabelDisplay='auto',
                           defaultValue=CustomHab.MissionDuration,
                           onChange=self.update_occ)
            ],

            mui.FormGroup[
                mui.FormLabel["Mission Duration [Years]"],
                mui.Slider(min=1,
                           max=5,
                           valueLabelDisplay='auto',
                           defaultValue=CustomHab.MissionDuration,
                           onChange=self.update_dur)
            ],

            html.code['Maximum Print Height [m]'],
                layout.SlotIntField(CustomHab, 'MaxPrintHeight'),

            mui.Button(variant='contained',
                       onClick=self.get_step)["Download .STEP file"],

            mui.Button(variant='contained',
                       onClick=self.get_stl)["Download .STL file"]
        ]

    def get_step(self, evt):
        writer1 = STEPWriter([CustomHab.habitat_geometry])
        assets_dir = get_assets_dir()
        fname = os.path.join(assets_dir, "Habitat.step")

        writer1.write(fname)

    def get_stl(self, evt):
        writer2 = STLWriter([CustomHab.habitat_geometry])
        assets_dir = get_assets_dir()
        fname = os.path.join(assets_dir, "Habitat.stl")

        writer2.write(fname)

    def update_occ(self,evt,value,idx):
        CustomHab.NumberOfOccupants = value

    def update_dur(self,evt,value,idx):
        CustomHab.MissionDuration = value

class OutputDialogs(Component):
    def render(self) -> NodeType:
        return layout.Box(orientation='vertical',
                          gap='1em',
                          style={'padding': '1em'})[
            mui.Paper(style={'width': '400px', 'padding': '1em'}, variant='outlined')[
                html.code['Printer Regolith Deposition Rate [kg/hr]'], layout.SlotIntField(
                    CustomHab, 'DepoRate'),
                mui.Typography[
                    f"Estimated Print Time: {round((round(CustomHab.print_volume, 2) * self.RegolithDensity()) / (CustomHab.DepoRate * 24), 2)} Days"],
                mui.Typography[
                    f"Number of Solar Panels: {CustomHab.life_support.Power.get_power_generation[0]}"],
                mui.Typography[
                    f"Number of Nuclear Fission Reactors: {CustomHab.life_support.Power.get_power_generation[1]}"]
            ],
            mui.Paper(style={'width': '400px', 'padding': '1em'}, variant='outlined')[
                mui.Typography[f"Geometric Overview"],
                mui.Divider,
                mui.Typography[f"Hab Wall Thickness: {round(CustomHab.life_support.Heating.t_min, 2)} m"],
                mui.Typography[f"Floors: {CustomHab.build_height}"],
                mui.Typography[f"Hab Height: {CustomHab.hab_height} m"],
                mui.Typography[f"Base Radius: {CustomHab.base_radius} m"],
                mui.Typography[f"Top Radius: {CustomHab.roof_radius} m"],
                mui.Typography[f"Estimated Print Volume: {round(CustomHab.print_volume, 2)} m^3"]
            ],
            mui.Paper(style={'width': '400px', 'padding': '1em'}, variant='outlined')[
                mui.Typography[f"Power Usage"],
                mui.Divider,
                mui.Typography[f"Science Module: {round(0.001 * CustomHab.science_module.get_science_power, 1)} kW"],
                mui.Typography[
                    f"Communications Module: {round(0.001 * CustomHab.communications.get_comms_power, 1)} kW"],
                mui.Typography[f"Repair Module: {round(0.001 * CustomHab.repair_workshop.get_workshop_power, 1)} kW"],
                mui.Typography[f"Airlock: {round(0.001 * CustomHab.airlock.get_airlock_power, 1)} kW"],
                mui.Typography[f"Living Quarters: {round(0.001 * CustomHab.living_quarters.get_livquart_power, 1)} kW"],
                mui.Typography[f"Life Support: {round(0.001 * CustomHab.life_support.get_lifesup_power, 1)} kW"],
                mui.Typography[f"Heating: {round(0.001 * CustomHab.life_support.Heating.Q_heat, 1)} kW"],
                mui.Divider,
                mui.Typography[f"Total Power Consumption: {round(0.001 * (CustomHab.get_tot_power_req + CustomHab.life_support.Heating.Q_heat),2)} kW"]
            ],
            mui.Paper(style={'width': '400px', 'padding': '1em'}, variant='outlined')[
                mui.Typography[f"Volume Distribution"],
                mui.Divider,
                mui.Typography[f"Science Module: {round(CustomHab.science_module.get_science_volume, 1)} m3"],
                mui.Typography[f"Communications Module: {round(CustomHab.communications.get_comms_volume, 1)} m3"],
                mui.Typography[f"Storage: {round(CustomHab.storage_module.get_storage_volume, 1)} m3"],
                mui.Typography[f"Repair Module: {round(CustomHab.repair_workshop.get_workshop_volume, 1)} m3"],
                mui.Typography[f"Airlock: {round(CustomHab.airlock.get_airlock_volume, 1)} m3"],
                mui.Typography[f"Living Quarters: {round(CustomHab.living_quarters.get_livquart_volume, 1)} m3"],
                mui.Typography[f"Life Support: {round(CustomHab.life_support.get_lifesup_volume, 1)} m3"],
                mui.Divider,
                mui.Typography[f"Total Habitat Volume: {CustomHab.get_tot_use_vol} m3"]
            ],
            mui.Paper(style={'width': '400px', 'padding': '1em'}, variant='outlined')[
                mui.Typography[f"Life Support Data"],
                mui.Divider,
                mui.Typography[f"Oxygen Module: {round(0.001*CustomHab.life_support.Oxygen.get_oxygen_power, 1)} kW, " \
                               f"{round(CustomHab.life_support.Oxygen.get_oxygen_volume, 1)} m3"],
                mui.Typography[f"Water Module: {round(0.001 * CustomHab.life_support.Water.get_system_power, 1)} kW, " \
                               f"{round(CustomHab.life_support.Water.get_system_volume, 1)} m3"],
                mui.Typography[f"Food Module: {round(0.001 * CustomHab.life_support.Food.get_farm_power, 1)} kW, " \
                               f"{round(CustomHab.life_support.Food.get_farm_volume, 1)} m3"]
            ]
        ]

    def RegolithDensity(self):
        if CustomHab.Body == "Moon":
            return 2500
        elif CustomHab.Body == "Mars":
            return 1800

class Piecharts(Component):
    def render(self) -> NodeType:
        TRACE_1 = {
            "values": [CustomHab.science_module.get_science_power,
                       CustomHab.communications.get_comms_power,
                       CustomHab.repair_workshop.get_workshop_power,
                       CustomHab.airlock.get_airlock_power,
                       CustomHab.living_quarters.get_livquart_power,
                       CustomHab.life_support.get_lifesup_power,
                       round(CustomHab.life_support.Heating.Q_heat)],
            "type": 'pie',
            "labels": ["Science", "Comms", "Workshop", "Airlock", "Living Quarters", "Life Support", "Heating"],
            "textinfo": "label+percent",
            "textposition": 'outside',
            "outsidetextorientation": 'radial',
            "hole": 0.4,
        }

        TRACE_2 = {
            "values": [CustomHab.science_module.get_science_volume,
                       CustomHab.communications.get_comms_volume,
                       CustomHab.storage_module.get_storage_volume,
                       CustomHab.repair_workshop.get_workshop_volume,
                       CustomHab.airlock.get_airlock_volume,
                       CustomHab.living_quarters.get_livquart_volume,
                       CustomHab.life_support.get_lifesup_volume],
            "type": 'pie',
            "labels": ["Science", "Comms", "Storage", "Workshop", "Airlock", "Living Quarters", "Life Support"],
            "textinfo": "label+percent",
            "textposition": 'outside',
            "outsidetextorientation": 'radial',
            "hole": 0.4,
        }
        return layout.Box(orientation='vertical',
                          gap='1em',
                          style={'padding': '1em'})[
        plotly.Plot(
            data=[TRACE_1],
            layout={
                "title": 'Power Consumption',
                "annotations": [
                    {
                        "font": {"size": 20},
                        "text": "Power",
                        "showarrow": False
                    }
                ]
            },
            config={'displaylogo': False},
            style={'height': '100%', 'width': '100%'},
            useResizeHandler=True
        ),

        plotly.Plot(
            data=[TRACE_2],
            layout={
                "title": 'Volume Distribution',
                "annotations": [
                    {
                        "font": {"size": 20},
                        "text": "Volume",
                        "showarrow": False
                    }
                ]
            },
            config={'displaylogo': False},
            style={'height': '100%', 'width': '100%'},
            useResizeHandler=True
        )
        ]


if __name__ == '__main__':
    from parapy.webgui.core import display
    display(Habitect, reload=True, assets_dir=DIR)
