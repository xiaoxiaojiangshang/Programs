%function [hole] = Judge_hole_intersect(hole)
row=size(hole,1);
%%����һ����Ϊ�ж��Ƿ��ظ���־
hole(:,10)=false;
C=(1:row);
for i=1:row-1
    for j=i+1:row
           A=hole(i,1:6);
           B=hole(j,1:6);
           [flag]=judge_position(A,B);
           % flag==1,˵���������ཻ
           if flag
               C(j)=C(i);
       end
    end
end

%end
