function timerCallback(src, eventdata, dirName, dirLength,fileName)
persistent my_dirLength;
persistent my_beginFlag;
persistent fileName1;
if isempty(my_beginFlag)
      my_dirLength = dirLength;
      my_beginFlag = 0;
      fileName1=fileName;
end
if length(dir(dirName)) > my_dirLength
disp('A new file is available')
      my_dirLength = length(dir(dirName));
% update
    fileFolder=fullfile(dirName);
    dirOutput=dir(fullfile(fileFolder,'*'));
    fileName2={dirOutput.name}';
%     save fileName2.mat fileName2;
%     save fileName1.mat fileName1;
    new_file=setdiff(fileName2,fileName1)
    fileName1=fileName2;
    for i=1:length(new_file)
        str=new_file{i};
        if(strfind(str,'.'))
            str=str
        else
            fileFolder=fullfile(str);
            dirOutput=dir(fullfile(fileFolder,'*'));
            fileName2={dirOutput.name}';
            fileName2(1:2)=[]
        end
    end
% disp(new_file);
else
disp('No new files')
end
