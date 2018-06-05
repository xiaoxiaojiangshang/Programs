function [] = dotCorFile2dotUtmFile(filepath)

if isdir(filepath)==0
    return;
end

[outDir,outArray,flag] =getDotCorFile(filepath);
%%导入处理数据
if flag
    for iOutDir=1:length(outDir)
        for jOutArray=1:length(outArray{iOutDir})
            importdata([filepath,'\',outDir{iOutDir},'\',outArray{iOutDir}{jOutArray}]);
            jOutArray_dotCorData=ans.textdata;
            dotUtmData=zeros(length(jOutArray_dotCorData(:,1:1)),3);
            dotUtmData(:,1:1)=str2num(char(jOutArray_dotCorData(:,1:1)));
            [dotUtmData(:,3:3),dotUtmData(:,2:2),zone]=deg2utm(str2num(...
            char(jOutArray_dotCorData(:,4:4))),str2num(char(jOutArray_dotCorData(:,6:6))));
            txt_name=[filepath,'\',outDir{iOutDir},'\',outArray{iOutDir}{jOutArray}(1:end-3),'utm'];
            %%保持一致
            deleteSpaceZone=strrep(zone(1,:), ' ', '');
            fid=fopen(txt_name,'w');
            invalidData=1;
            for jDataRow=1:length(dotUtmData(:,1:1))
              fprintf(fid,'%d %f %f %d %s\r\n',dotUtmData(jDataRow,:),invalidData,deleteSpaceZone);  
            end
        end
    end
else return;
end
end