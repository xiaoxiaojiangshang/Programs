 function [Data] = Show(F,Start,End)
 
 %%%% �ӵ�ǰ�ļ��¶�ȡ����
 F1=[F,'Data.mat'];
 F2=[F,'Abnormal.mat'];
%  Data=load(F1);
%  Abnormal=load(F2);
%  hole=Abnormal.hole;
%  Data=Data.P;
load(F1);
load(F2);
%%%��ȡ���ݲ���ֵ
Data=P(:,Start:End,:);
Data=interpolation(Data);
[row,~]=size(hole);
 %%% �ж��Ƿ���ڣ�����0��1��
 black=min(Data(:));
 white=max(Data(:));
 colors=[black,white];
 if(size(hole)~=0)
     for i=1:row
        flag=0;
        [y1,y2,flag]=Judge(Start,End,hole(i,2),hole(i,5));
       %%% flag==1,����hole������һ�����ڽ�ȡ��λ
        if(flag)
            %x1,y1,z1,x2,y2,z2 -> 1,2,3,4,5,6
            %����
            Data(hole(i,1):hole(i,1)+3,y1:y2,hole(i,3):hole(i,6))=colors(hole(i,7)+1);
            %����
            Data(hole(i,4)-3:hole(i,4),y1:y2,hole(i,3):hole(i,6))=colors(hole(i,7)+1);
            %����
            Data(hole(i,1):hole(i,4),y1:y1+3,hole(i,3):hole(i,6))=colors(hole(i,7)+1);
            %����
            Data(hole(i,1):hole(i,4),y2-3:y2,hole(i,3):hole(i,6))=colors(hole(i,7)+1);
            %ǰ��
            Data(hole(i,1):hole(i,4),y1:y2,hole(i,3):hole(i,3)+3)=colors(hole(i,7)+1);
            %����
            Data(hole(i,1):hole(i,4),y1:y2,hole(i,6)-3:hole(i,6))=colors(hole(i,7)+1);
        end
     end  
 end 
 end
