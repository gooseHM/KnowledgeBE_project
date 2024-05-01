%%% thickness optimization as a function of Qmax
% intializing
function output = t_opt(input)
k_con_mars = 0.039;
GL_V = input(1);
% GL_H = input(2);
% GR_V = input(3);

% Q_sys = input(4);
Q_max_HR = input(5);
% Q_s = input(6);
% 
% T_ex = input(7);
% T_in = input(8);


A_vertical = input(9);


t_initial = A_vertical*k_con_mars/GL_V;
dt = 0.01; %m 

t = t_initial;
Q_heater = Q_max_HR*2;

while Q_heater >= Q_max_HR
    
    Q_TT = Habitat_thermal_model(input);
    Q_heater = Q_TT(1);
    %x1 = Qheat x2 = T_V x3 = T_H
    t = t + dt;
    GL_V = k_con_mars*A_vertical/t;
    input(1) = GL_V;
end




output = [Q_TT(1),t];

end