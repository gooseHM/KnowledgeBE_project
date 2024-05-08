%%% thickness optimization as a function of Qmax
% intializing
function output = t_opt(input)
k_con_mars = 0.039;
GL_V = input(1);
Q_max_HR = input(5);
A_vertical = input(9);

% Initialization
t_initial = A_vertical*k_con_mars/GL_V;
dt = 0.01; %m
t = t_initial;
Q_heater = Q_max_HR*2;

while Q_heater >= Q_max_HR
    % Calculates the wall thickness needed to reach the desired temperature inside the Habitat.
    % Making sure the Heating power used stays within the given bounds
    
    Q_TT = Habitat_thermal_model(input);
    Q_heater = Q_TT(1);
    %x1 = Qheat x2 = T_V x3 = T_H
    t = t + dt;
    GL_V = k_con_mars*A_vertical/t;
    input(1) = GL_V;
end

output = [Q_TT(1),t];

end