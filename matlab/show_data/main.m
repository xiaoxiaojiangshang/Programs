F='20171201西津西路下立交东入口至兰州西站_000_';
show_data=Show(F,11000,11800);
for i=44:54
data=show_data(:,:,i);
%data1=reshape(data,501,121);
figure;imshow(data,[]);
end
