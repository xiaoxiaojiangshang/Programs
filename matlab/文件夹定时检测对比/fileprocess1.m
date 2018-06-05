function [OutDir,Outarray] = fileprocess1(filepath)
if isdir(filepath)==0
    return;
end
dirOut=dir(fullfile(filepath,'*'));
filearray={dirOut.name
};
j=1;
for i=3:size(filearray,2)
    ff = fullfile(filepath,filearray{i});
    if isdir(ff)
      dirOut=dir(fullfile(ff,'*_Data*'));
        Outarray{j}={dirOut.name   
        };
    for k=1:size(Outarray{j},2)
        Outarray{j}{k}=Outarray{j}{k}(1:(end-9));
    end
    OutDir{j}=filearray{i};
    j=j+1;
    end
end
