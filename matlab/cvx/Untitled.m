% m = 16;n = 8;
% A = randn(m,1);
% B=[A.^2,A];
% b=A.^2*3+2*A+5;
% cvx_begin
%     variable x(3,1);
%     minimize( norm(B*x(1:2,1)+x(3,1) - b) )
% cvx_end
