function [x,y]=coordinateTransform(xSource,ySource,yEnd,alpha)
% -1==left 1==right
d=yEnd-ySource;
y=ySource+d*cosd(alpha);
x=xSource+abs(d)*sind(alpha);
