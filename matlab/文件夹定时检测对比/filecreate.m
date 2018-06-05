function filecreate(rootpath,DirArray)
if isdir(rootpath)==0
    return;
end
for i=1:size(DirArray,2)
    mkdir(fullfile(rootpath,DirArray{i}));
end