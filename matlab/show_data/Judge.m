function [y1,y2,flag] = Judge(Start,End,ymin,ymax)
flag=1;
if(ymin>=End || ymax<=Start)
    flag=0;
    y1=0;
    y2=0;
else y1=max(Start,ymin)-Start+1;
    y2=min(End,ymax)-Start+1;
end
end
