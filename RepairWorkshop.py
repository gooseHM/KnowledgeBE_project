from parapy.core import *


class Repair(Base):

    @Attribute
    def printer(self):                                          # small 3D printer for internal parts and repairs
        printer_volume = 1.5*1*2
        printer_power = 650
        return printer_volume, printer_power

    @Attribute
    def spares_storage(self):                                   # spare parts stored in workshop
        storage_volume = 2*1*3
        return storage_volume

    @Attribute
    def tools(self):                                            # tooling space
        tools_volume = 0.5
        return tools_volume

    @Attribute
    def workbench(self):                                        # work area
        workbench_volume = 1*2*1
        workbench_power = 1000
        return workbench_volume, workbench_power

    @Attribute
    def get_workshop_volume(self):
        return self.printer[0] + self.spares_storage + self.tools + self.workbench[0]

    @Attribute
    def get_workshop_power(self):
        return self.printer[1] + self.workbench[1]


if __name__ == '__main__':
    from parapy.gui import display
    obj = Repair(label='Repair Workshop')
    display(obj)
