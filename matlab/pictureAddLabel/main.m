for iFile=1:length(filearray)
    fileCompetePath=[filepath,'\',filearray{iFile}]
    picture=imread(fileCompetePath);
    pictureAddLabel=bmpAddLabel(picture,301);
    imshow(pictureAddLabel);
    pause(4);
    close;
end
 