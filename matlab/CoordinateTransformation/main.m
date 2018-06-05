
warning off
% 椭圆上的点(1)
x=[-2.83249,-2.45957,-1.97861,-1.39136,-0.719151,0,0.719151,1.39136,1.97861,2.45957,2.83249];
y=[2.88173,2.63417,2.39273,2.18734,2.04888,2,2.04888,2.18734,2.39273,2.63417,2.88173];

% 椭圆上的点(2)
% x=[-0.783509,-0.672342,-0.538472,-0.37957,-0.197236,0,0.197236,0.37957,0.538472,0.672342,0.783509];
% y=[3.44179,3.31824,3.19997,3.09764,3.02605,3,3.02605,3.09764,3.19997,3.31824,3.44179];

% xSource=[-5,-4,-3,-2,-1,0,1,2,3,4,5];
% ySource=zeros(size(xSource));

xSource=linspace(-5,5,11);
ySource=zeros(size(xSource));

xEnd=x;
yEnd=y;

temp=(xSource-xEnd).*(xSource-xEnd)+yEnd.*yEnd;
yEnd=sqrt(temp);

x=linspace(-5,5,30);

yEnd=spline(xSource,yEnd,x);
xSource=x;
ySource=zeros(size(xSource));

noise=wgn(size(yEnd,1),size(yEnd,2),1)/50;
yEnd=noise+yEnd;

k=3/4;
dataN=length(xSource);
%中间变量
%从左向中间角度依次减小
deflectAngles=zeros(1,dataN);
leftRight=zeros(1,dataN);

% 直线与椭圆交点
intersectX=zeros(1,dataN);
intersectY=zeros(1,dataN);

%线段偏转角度后所xEnd和yEnd所在的点
tempX=zeros(1,dataN);
tempY=zeros(1,dataN);

errorAngle=zeros(1,dataN);
count=0;

angleStep=5;

angleChange=zeros(1,dataN);



interNum=0;
while(1)
    interNum=interNum+1;
    for iCount=1:dataN
        [tempX(iCount),tempY(iCount)]=coordinateTransform(xSource(iCount),ySource(iCount),yEnd(iCount),deflectAngles(iCount));
    end
    %fittling
    figure;
    plot(tempX,tempY,'*')
    
    for kk=1:dataN
        hold on,line([xSource(kk),tempX(kk)],[ySource(kk),tempY(kk)]);
    end
    
    [A,B,X0,Y0]=EllipseFitK(tempX',tempY',k);
    
    X=(X0-A):0.01:(X0+A);
    X=X';
    Y=-sqrt(B^2*((1-(X-X0).^2./A^2)))-Y0;
    Y1=sqrt(B^2*((1-(X-X0).^2./A^2)))-Y0;
    %   figure;
    hold on;
    plot(X,Y,'b');
    hold on;
    plot(X,Y1,'b');
    hold on;    
    drawnow;
    for iCount=1:dataN
        [intersectX(iCount),intersectY(iCount)]=ellipseIntersect(xSource(iCount),ySource(iCount),tempX(iCount),tempY(iCount),A,B,X0,Y0);
        % 实数，相交
        if(isreal(intersectX(iCount)))
            K=-(B^2/A^2)*((intersectX(iCount)+X0)/(intersectY(iCount)+Y0));
            
            alpha=twoLineAngle(xSource(iCount),ySource(iCount),intersectX(iCount),intersectY(iCount),intersectX(iCount)+1,intersectY(iCount)+K);
            alp(iCount)=alpha;
            angleChange(iCount)=90-alpha;
            errorAngle(iCount)=abs(alpha-90);
            if alpha>90
                leftRight(iCount)=-1;
            else
                leftRight(iCount)=1;
            end
        else
            ans=intersectX(iCount)
            %angleChange(iCount)=0;
            pause(3)
        end
    end

    MeanError=sum(errorAngle)/dataN
    Error(interNum)=MeanError;
    if MeanError<0.5
        break;
    else
        deflectAngles= deflectAngles+angleChange;
    end
end




