function [X,Y]=ellipseIntersect(x1,y1,x2,y2,a,b,x0,y0)

if x1==x2
    equationStr=['x==',num2str(x1)];
else
    k=(y2-y1)/(x2-x1);
    bb=y1-k*x1;
    equationStr=['y==',num2str(k),'*x+',num2str(bb)];
end

syms x y;
s=solve((x+x0)^2/a^2+(y+y0)^2/b^2==1,equationStr,x,y);
temp1=double(s.x);
temp2=double(s.y);

if(length(temp1)>1)
    if (temp1(1)-x1)^2+(temp2(1)-y1)^2>(temp1(2)-x1)^2+(temp2(2)-y1)^2
        X=temp1(2);
        Y=temp2(2);
    else
        X=temp1(1);
        Y=temp2(1);
    end
else
    X=temp1(1);
    Y=temp1(2);
end
