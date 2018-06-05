function [ full_data ] = interpolation( data )

sz = size(data);
full_data = zeros(sz(1),sz(2),121);
xi = 0 : 8 : 120;
xx = 0:120;
M=sz(1);
N=sz(2);
for i = 1 : M
    disp(['Spline ',num2str(i)]);
    for j= 1 : N
        yi = data(i,j,:);
        %full_data(i,j,:) = interp1(xi,yi,xx,'spline');
        full_data(i,j,:) = spline(xi,yi,xx);
    end
end
end

