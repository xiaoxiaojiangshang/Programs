function [OutDir,Outarray,flag] =getDotCorFile(filepath)
OutDir={};
Outarray={};
flag=true;
if isdir(filepath)==0
    return;
end
dirOut=dir(fullfile(filepath,'*'));
filearray={dirOut.name
};
j=1;
if ~isempty(filearray)
    for i=3:size(filearray,2)
    ff = fullfile(filepath,filearray{i});
    if isdir(ff)
      dirOut=dir(fullfile(ff,'*.cor'));
        Outarray{j}={dirOut.name   
        };
    for k=1:size(Outarray{j},2)
        Outarray{j}{k}=Outarray{j}{k};
    end
    OutDir{j}=filearray{i};
    j=j+1;
    end
    end
else flag=false;
end
end
