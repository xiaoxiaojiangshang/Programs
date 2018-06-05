function [flag]=judge_position(A,B)
% 获得B的八个点
Ax=[min(A(1),A(4)),max(A(1),A(4))];
Ay=[min(A(2),A(5)),max(A(2),A(5))];
Az=[min(A(3),A(6)),max(A(3),A(6))];

Bx=[B(1),B(4)];
By=[B(2),B(5)];
Bz=[B(3),B(6)];
flag=false;

for i=1:2
    for j=1:2
        for k=1:2
           if Bx(i)<=Ax(2)&&Bx(i)>=Ax(1)&&By(j)<=Ay(2)&&By(j)>=Ay(1)&&Bz(k)<=Az(2)&&Bz(k)>=Az(1)
                flag=true;
                 break;
            end
        end
    end
end


