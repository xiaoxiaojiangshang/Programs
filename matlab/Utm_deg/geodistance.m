function r = geodistance( ci , cf , m )  
 
% Calculates the distance in meters between two points on earth surface. 
% 
% SYNTAX: r = geodistance( coordinates1 , coordinates2 , method ) ;  
%          
%          Where coordinates1 = [longitude1,latitude1] defines the 
%          initial position and coordinates2 = [longitude2,latitude2] 
%          defines the final position. 
%          Coordinates values should be specified in decimal degrees. 
%          Method can be an integer between 1 and 23, default is m = 6.  
%         Methods 1 and 2 are based on spherical trigonometry and a  
%         spheroidal model for the earth, respectively.   
%          Methods 3 to 23 use Vincenty's formulae, based on ellipsoid  
%         parameters.  
%         Here it follows the correspondence between m and the type of  
%         ellipsoid: 
% 
%         m =  3 -> ANS ,        m =  4 -> GRS80,    m = 5 -> WGS72,  
%         m =  6 -> WGS84,       m =  7 -> NSWC-9Z2,  
%         m =  8 -> Clarke 1866, m =  9 -> Clarke 1880, 
%         m = 10 -> Airy 1830,   
%         m = 11 -> Bessel 1841 (Ethiopia,Indonesia,Japan,Korea), 
%         m = 12 -> Bessel 1841 (Namibia), 
%         m = 13 -> Sabah and Sarawak (Everest,Brunei,E.Malaysia), 
%         m = 14 -> India 1830, m = 15 -> India 1956,  
%         m = 16 -> W. Malaysia and Singapore 1948,  
%         m = 17 -> W. Malaysia 1969,  
%         m = 18 -> Helmert 1906,m = 19 -> Helmert 1960, 
%         m = 20 -> Hayford International 1924,  
%         m = 21 -> Hough 1960, m = 22 -> Krassovsky 1940, 
%         m = 23 -> Modified Fischer 1960,  
%         m = 24 -> South American 1969.  
% 
%          Important notes: 
% 
%         1)South latitudes are negative. 
%         2)East longitudes are positive. 
%         3)Great circle distance is the shortest distance between two points  
%          on a sphere. This coincides with the circumference of a circle which  
%          passes through both points and the centre of the sphere. 
%         4)Geodesic distance is the shortest distance between two points on a spheroid. 
%         5)Normal section distance is formed by a plane on a spheroid containing a  
%          point at one end of the line and the normal of the point at the other end.  
%          For all practical purposes, the difference between a normal section and a  
%          geodesic distance is insignificant. 
%         6)The method m=2 assumes a spheroidal model for the earth with an average  
%          radius of 6364.963 km. It has been derived for use within Australia.  
%          The formula is estimated to have an accuracy of about 200 metres over 50 km,  
%          but may deteriorate with longer distances.  
%          However, it is not symmetric when the points are exchanged.  
%   
%  Examples: A = [150 -30]; B = [150 -31]; L = [151 -80]; 
%            [geodistance(A,B,1) geodistance(A,B,2) geodistance(A,B,3)] 
%            [geodistance(A,L,1) geodistance(A,L,2) geodistance(A,L,3)] 
%            geodistance([0 0],[2 3]) 
%            geodistance([2 3],[0 0]) 
%            geodistance([0 0],[2 3],1) 
%            geodistance([2 3],[0 0],1) 
%            geodistance([0 0],[2 3],2) 
%            geodistance([2 3],[0 0],2) 
%            for m = 1:24 
%            r(m) = geodistance([150 -30],[151 -80],m); 
%            end 
%            plot([1:m],r), box on, grid on 
 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
% Second version: 07/11/2007 
%  
% Contact: orodrig@ualg.pt 
%  
% Any suggestions to improve the performance of this  
% code will be greatly appreciated.  
%  
% Reference: Geodetic Calculations Methods 
%            Geoscience Australia 
%            (http://www.ga.gov.au/geodesy/calcs/) 
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
 
r = [ ] ;  
 
if nargin == 2, m = 6; end  
 
longitude1 = pi*ci(1)/180 ;  
 latitude1 = pi*ci(2)/180 ;  
  
longitude2 = pi*cf(1)/180 ;  
 latitude2 = pi*cf(2)/180 ;  
 
alla = [0 0 6378160 6378137.0 6378135 6378137.0 6378145 6378206.4 6378249.145,... 
          6377563.396 6377397.155 6377483.865,...  
          6377298.556 6377276.345 6377301.243 6377304.063 6377295.664 6378200 6378270 6378388  6378270 6378245,...  
          6378155 6378160]; 
 
allf = [0 0  1/298.25 1/298.257222101 1/298.26 1/298.257223563 1/298.25 1/294.9786982 1/293.465,... 
             1/299.3249646 1/299.1528128,... 
             1/299.1528128 1/300.8017 1/300.8017 1/300.8017 1/300.8017 1/300.8017 1/298.3 1/297 1/297 1/297,...   
             1/298.3 1/298.3 1/298.25]; 
 
if ( longitude1 == longitude2)&&( latitude1 == latitude2 )  
 
r = 0;  
 
else  
 
if m == 1 % Great Circle Distance, based on spherical trigonometry 
 
       r = 180*1.852*60*acos( ... 
       sin(latitude1)*sin(latitude2) + cos(latitude1)*cos(latitude2)*cos(longitude2-longitude1) )/pi ; 
       r = 1000*abs( r );   
 
elseif m == 2 % Spheroidal model for the earth  
 
       term1 = 111.08956*( ci(2) - cf(2) + 0.000001 ) ;   
       term2 = cos( latitude1  + ( (latitude2 - latitude1)/2 ) ) ; 
       term3 = ( cf(1) - ci(1) + 0.000001 )/( cf(2) - ci(2) + 0.000001 ) ;   
       r = 1000*abs( term1/cos( atan( term2*term3 ) ) );  
 
else % Apply Vincenty's formulae (as long as the points are not coincident): 
 
a = alla(m);  
f = allf(m);  
 
b = a*( 1 - f ) ;                                                                                                  
 
tangens_u1 = ( 1 - f )*tan( latitude1 ) ; u1 = atan( tangens_u1 ) ;                                                  
tangens_u2 = ( 1 - f )*tan( latitude2 ) ; u2 = atan( tangens_u2 ) ;                                                  
delta_longitude = longitude2 - longitude1 ;                                                                          
lambda = delta_longitude ;                                                                                          
squared_sin_of_sigma = ( cos(u2)*sin(lambda) )^2 + ( cos(u1)*sin(u2) - sin(u1)*cos(u2)*cos(lambda) )^2 ;          
        sin_of_sigma = sqrt( squared_sin_of_sigma ) ; % This is zero when the points are coincident...                                                                   
        cos_of_sigma = sin( u1 )*sin( u2 ) + cos( u1 )*cos( u2 )*cos( lambda ) ;                                  
        tan_of_sigma = sin_of_sigma/cos_of_sigma ;                                                                  
               sigma = atan( tan_of_sigma ) ;                                                                          
    tangens_of_sigma = sin_of_sigma/cos_of_sigma ;                                                          
        sin_of_alpha = cos( u1 )*cos( u2 )*sin( lambda )/sin_of_sigma ;                                           
        cos_of_alpha = sqrt( 1 - sin_of_alpha^2 ) ;                                                                  
        cos_of_2sigmam = cos_of_sigma - ( 2*sin( u1 )*sin( u2 )/cos_of_alpha^2 ) ;                                  
                                                                                                           
C = (f/16)*( cos_of_alpha )^2*( 4 + f*( 4 - 3*( cos_of_alpha )^2 ) ) ;                                                  
 
lambda2 = delta_longitude + ( 1 - C )*f*sin_of_alpha*( sigma + C*sin_of_sigma*( ...                                  
           cos_of_2sigmam + C*cos_of_sigma*( -1 + 2*( cos_of_2sigmam )^2 ) ) ) ;                                  
 
while ( abs( lambda - lambda2 ) > 1e-9 )                                                                          
                                                                                                                   
 lambda = lambda2 ;                                                                                                  
 squared_sin_of_sigma = ( cos(u2)*sin(lambda) )^2 + ( cos(u1)*sin(u2) - sin(u1)*cos(u2)*cos(lambda) )^2 ;         
         sin_of_sigma = sqrt( squared_sin_of_sigma ) ;                                                                  
         cos_of_sigma = sin( u1 )*sin( u2 ) + cos( u1 )*cos( u2 )*cos( lambda ) ;                                  
         tan_of_sigma = sin_of_sigma/cos_of_sigma ;                                                                  
                sigma = atan( tan_of_sigma ) ;                                                                          
     tangens_of_sigma = sin_of_sigma/cos_of_sigma ;                                                                  
         sin_of_alpha = cos( u1 )*cos( u2 )*sin( lambda )/sin_of_sigma ;                                          
         cos_of_alpha = sqrt( 1 - sin_of_alpha^2 ) ;                                                                  
         cos_of_2sigmam = cos_of_sigma - ( 2*sin( u1 )*sin( u2 )/cos_of_alpha^2 ) ;                                  
                                                                                                           
 C = (f/16)*( cos_of_alpha )^2*( 4 + f*( 4 - 3*( cos_of_alpha )^2 ) ) ;                                           
                                                                                                           
 lambda2 = delta_longitude + ( 1 - C )*f*sin_of_alpha*( sigma + C*sin_of_sigma*( ...                                  
           cos_of_2sigmam + C*cos_of_sigma*( -1 + 2*( cos_of_2sigmam )^2 ) ) ) ;                                  
 
end % while ( abs(lambda - lambda2 ) > 1e-9 )                                                                          
 
u2 = ( cos_of_alpha^2 )*( a^2 - b^2 )/b^2 ;                                                                          
A = 1 + ( u2/16384 )*( 4096 + u2*( -768 + u2*( 320 - 175*u2 ) ) ) ;                                                  
B = ( u2/1024 )*( 256 + u2*( -128 + u2*( 74 - 47*u2 ) ) ) ;                                                          
delta_sigma = B*sin_of_sigma*( cos_of_2sigmam + ( B/4 )*( ...                                                          
                cos_of_sigma*( -1 + 2*cos_of_2sigmam^2 ) - ...                                                          
          (B/6)*cos_of_2sigmam*( -3 + 4*sin_of_sigma^2 )*( -3 + 4*cos_of_2sigmam^2 ) ) ) ;                          
r = b*A*( sigma - delta_sigma ) ;                                                                                   
 
end  
 
end