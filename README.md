Mars habitat prelimanary design configurator
_INSTRUCTIONS:_

_Used extensions and software packages_
- Excel
- Matlab R2024a
optimization toolbox
- parapy 1.11.2
- Python 3.11, notably extensions:
  matlabengine 24.1 , numpy 1.26.4 & openpyxl 3.1.2

![image](https://github.com/gooseHM/KnowledgeBE_project/assets/128814624/8a9d8634-0176-408f-bbbd-06a947d83a7c)



1. Start out with loading the Excel input file named "Habitat_Design_Specification.xlsx"

Inputs are in the L through P columns the most important ones are:
- Number of occupants,                    driving most of the volume and power requirements.
- Staying time,                           driving the importance of food production.
- Design for Moon or Mars,                driving the environmental consideration.
- Max print height                        driving the geometry limits

2. Close & SAVE! the excel file, run the HAB001 python file
   & instantiate the Habitat root object. 

3. configure design to an instance & safe by clicking the safe_output atribute in the Habitat object.
4. Find the outputs in the excel file by opening them 





