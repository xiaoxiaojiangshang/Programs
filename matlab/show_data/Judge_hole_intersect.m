%function [hole] = Judge_hole_intersect(hole)
row=size(hole,1);
%%增加一列作为判断是否重复标志
hole(:,10)=false;
C=(1:row);
for i=1:row-1
    for j=i+1:row
           A=hole(i,1:6);
           B=hole(j,1:6);
           [flag]=judge_position(A,B);
           % flag==1,说明这两个相交
           if flag
               C(j)=C(i);
       end
    end
end

%end
