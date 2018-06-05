function [A,B,Y0]=ellipseFit(x,y,k)

S=[x.*x,y.*y,y,ones(size(x))];
SS=S'*S;

cvx_begin
variable v(4);
minimize(v'*SS*v)

subject to
v(1)==k^2;
v(2)==1;
% v(3)<0;
v(4)>0;
cvx_end
Y0=v(3)/2;
A=sqrt((v(3)/2)^2-v(4))/k;
B=k*A;

% function [A,B,X0,Y0]=ellipseFit(x,y)
% 
% S=[x.*x,y.*y,x,y,ones(size(x))];
% SS=S'*S;
% 
% cvx_begin
% variable v(5);
% minimize(v'*SS*v)
% subject to
% v(1)>0;
% v(2)>0;
% cvx_end
% 
% temp=v(3)*v(3)/(v(1)*v(1)*v(2)*4)+v(4)*v(4)/(v(1)*v(2)*v(2)*4)-v(5)/(v(1)*v(2));
% A=sqrt(v(2)/temp);
% B=sqrt(v(1)/temp);
% X0=v(3)/2/v(1);
% Y0=v(4)/2/v(2);
