 function  [Lat,Lon] = Transform(VarName3,VarName2,loc)
Len=length(VarName2);
% from utm to deg
for i=1:Len
    utmzone(i,:)='48 S';
end
[Lat, Lon]=Utm2deg(VarName3,VarName2,utmzone); 

%find the location we want 
for i=1:Len
    if(VarName1(i)>loc)
       break;
    end
end

% Linear avg to get approximate len,lon
a=VarName1(i-1);
b=VarName1(i);
abs=loc-a;
c=b-a;
loc_lon=(Lon(i)-Lon(i-1))/c*abs+Lon(i-1);
loc_lat=(Lat(i)-Lat(i-1))/c*abs+Lat(i-1);
 end
        









