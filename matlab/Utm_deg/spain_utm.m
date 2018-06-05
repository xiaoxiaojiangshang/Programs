function  [b] = spain_utm(a)

i=1;
while(a(i,1)~=1)
   a(i,:)=[];
end
% ‘§œ»∏≥÷µ
Len=length(a);
scan_max=a(Len,1);
b=zeros(scan_max,5);
j=1;
for i=2:Len:
    x=[a(i-1),a(i)];
    t=a(i-1):a(i);
    y1=spline(x,[a(i-1),a(i)],t);
    y2=spline(x,[a(i-1,2),a(i,2)],t);
    y3=spline(x,[a(i-1,3),a(i,3)],t);
    else 
    
end

end