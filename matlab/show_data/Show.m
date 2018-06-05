 function [Data] = Show(F,Start,End)
 
 %%%% 从当前文件下读取数据
 F1=[F,'Data.mat'];
 F2=[F,'Abnormal.mat'];
%  Data=load(F1);
%  Abnormal=load(F2);
%  hole=Abnormal.hole;
%  Data=Data.P;
load(F1);
load(F2);
%%%截取数据并插值
Data=P(:,Start:End,:);
Data=interpolation(Data);
[row,~]=size(hole);
 %%% 判断是否存在，存在0黑1白
 black=min(Data(:));
 white=max(Data(:));
 colors=[black,white];
 if(size(hole)~=0)
     for i=1:row
        flag=0;
        [y1,y2,flag]=Judge(Start,End,hole(i,2),hole(i,5));
       %%% flag==1,代表hole至少有一部分在截取部位
        if(flag)
            %x1,y1,z1,x2,y2,z2 -> 1,2,3,4,5,6
            %上面
            Data(hole(i,1):hole(i,1)+3,y1:y2,hole(i,3):hole(i,6))=colors(hole(i,7)+1);
            %下面
            Data(hole(i,4)-3:hole(i,4),y1:y2,hole(i,3):hole(i,6))=colors(hole(i,7)+1);
            %左面
            Data(hole(i,1):hole(i,4),y1:y1+3,hole(i,3):hole(i,6))=colors(hole(i,7)+1);
            %右面
            Data(hole(i,1):hole(i,4),y2-3:y2,hole(i,3):hole(i,6))=colors(hole(i,7)+1);
            %前面
            Data(hole(i,1):hole(i,4),y1:y2,hole(i,3):hole(i,3)+3)=colors(hole(i,7)+1);
            %后面
            Data(hole(i,1):hole(i,4),y1:y2,hole(i,6)-3:hole(i,6))=colors(hole(i,7)+1);
        end
     end  
 end 
 end
