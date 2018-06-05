function [Add_file,Add_array] = Change(Dir1,Dir2,array1,array2)
Add_file={};
% Add_array={};
K=1;
%% 遍历文件夹
for i=1:length(Dir2)
    %判断有没有添加新的文件夹，有0无1
    if sum(strcmp(Dir1,Dir2{i}))
        %判断在原来文件夹的的位置n，如果添加或者删除新文件夹可能就不对应了
        n=find(strcmp(Dir1,Dir2{i}));
        %判断有没有新添内容，对应array{i}
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
        %对于新建文件夹，整个包含
          Add_array{K}=array2{i};
          K=K+1;
    end
end
end







 
