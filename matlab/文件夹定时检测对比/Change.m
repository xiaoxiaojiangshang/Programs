function [Add_file,Add_array] = Change(Dir1,Dir2,array1,array2)
Add_file={};
% Add_array={};
K=1;
%% �����ļ���
for i=1:length(Dir2)
    %�ж���û������µ��ļ��У���0��1
    if sum(strcmp(Dir1,Dir2{i}))
        %�ж���ԭ���ļ��еĵ�λ��n�������ӻ���ɾ�����ļ��п��ܾͲ���Ӧ��
        n=find(strcmp(Dir1,Dir2{i}));
        %�ж���û���������ݣ���Ӧarray{i}
        for j=1:length(array2{i})
            if sum(strcmp(array1{n},array2{i}{j}))==false
                diff_array=setdiff(array2{i},array1{n});
                Add_file=[Add_file,Dir2{i}];
                  Add_array{K}=diff_array;
                  K=K+1;
                break;
            end
        end           
    else Add_file=[Add_file,Dir2{i}];
        %�����½��ļ��У���������
          Add_array{K}=array2{i};
          K=K+1;
    end
end
end







 
