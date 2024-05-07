function [T]=Habitat_thermal_model(input)
%Define the system of equations: thermal balance

% Assigning values to variables
GL_V = input(1);
GL_H = input(2);
GR_V = input(3);

Q_sys = input(4);
Q_max_HR = input(5);
Q_sun = input(6);

T_ex = input(7)+273.15;
T_in = input(8)+273.15;


% A_vertical = input(9);
perc_Qsys = input(10)


%x1 = Qheat x2 = T_V x3 = T_H
eqs = @(x) [Q_sys*perc_Qsys + x(1) + GL_V*(x(2)-T_in) + GL_H*(x(3)-T_in);
            Q_sun + GL_V*(T_in-x(2))+GR_V*(T_ex^4 - x(2)^4);
            GL_H*(T_in-x(3))];


%Provide an initial guess (replace with actual values)
initial_guess = [Q_max_HR*2;...
                273.15;...
                273.15];

%Solve the system of equations using fsolve
[T] = fsolve(eqs, initial_guess,optimset('Display','off'))-273.15;

end