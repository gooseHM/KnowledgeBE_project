function out_QH_t = Thermal_sizing(input)
%%%

R_c = input(1);
R_e = input(2);
T_inside = input(3);
T_min = input(4);
A_base = input(5);
A_vertical = input(6);
t_base = input(7);
Q_sys = input(8);
Q_max = input(9)*Q_sys;
perc_Qsys = input(10)

t_v_init = 0.02;

% Assigning values to variables
 GL_V = GL(R_c,A_vertical,t_v_init);  
 GL_H = GL(R_c,A_base,t_base);
 GR_V = GR(R_e,A_vertical);
 
% Q_sys = input(4);
 Q_max_HR = Q_max;
 Q_s = 0;
% 
 T_ex = T_min;
 T_in = T_inside;
% 
% 
% A_vertical = input(9);


input_t_opt = [GL_V,GL_H,GR_V,...
         Q_sys,Q_max_HR,Q_s...
        T_ex,T_in,...
        A_vertical,perc_Qsys];

 out_QH_t = t_opt(input_t_opt);

  function GR = GR(eps, A)
    B_c = 5.67e-8; %[m2*kg/(s2*K)]
    GR = B_c*eps*A;
end

function GL = GL(k,A,L)
        GL = k*A/L;
end

end