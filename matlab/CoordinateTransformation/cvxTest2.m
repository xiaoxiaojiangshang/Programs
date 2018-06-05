%Ellipse x^2/16+(y-5)^2/9=1

a=4;
b=3;
y0=-5;
k=b/a;

x=-4:4:4;
x=x';
y=-sqrt(b^2*(1-x.^2./a^2))-y0;

n=wgn(size(x,1),size(x,2),1)*0.02;
y=y+n;


figure;
plot(x,y,'*');

[A,B,Y0]=ellipseFit(x,y,k);

S=[x.*x,y.*y,y,ones(size(x))];
SS=S'*S;

X=-4:0.01:4;
X=X';
Y=-sqrt(B^2*(1-X.^2./A^2))-Y0;

hold on; plot(X,Y);
