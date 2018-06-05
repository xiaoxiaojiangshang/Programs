function alpha=twoLineAngle(x1,y1,x2,y2,x3,y3)
vector1=[x1-x2,y1-y2];
vector2=[x3-x2,y3-y2];

cosValue=vector1*vector2';
denominator=sqrt(((x2-x1)^2+(y2-y1)^2)*((x2-x3)^2+(y2-y3)^2));

alpha=acosd(cosValue/denominator);

end