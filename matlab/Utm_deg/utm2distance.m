function[sum]=utm2distance(utm)
Len=length(utm);
% from utm to deg
for i=1:Len
    utmzone(i,:)='48 S';
end
[Lat, Lon]=Utm2deg(utm(:,3),utm(:,2),utmzone); 

sum=0;
for i=1:Len-1
    sum=sum+geodistance([Lat(i),Lon(i)],[Lat(i+1),Lon(i+1)],6);
end