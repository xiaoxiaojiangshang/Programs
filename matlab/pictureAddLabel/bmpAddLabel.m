function pictureAddLabel=bmpAddLabel(picture,position)

[row,column,~]=size(picture);
pictureAddLabel=picture;
pictureAddLabel(end-2:end,:,:)=0;

if column<600
    if position<=300
       pictureAddLabel=insertText(pictureAddLabel,[row-5,position],num2str(position));
       pictureAddLabel=insertText(pictureAddLabel,[row-5,position+150],num2str(position+150));
       pictureAddLabel=insertText(pictureAddLabel,[row-5,position+300],num2str(position+300));
    else 
       pictureAddLabel=insertText(pictureAddLabel,[row-5,position],num2str(position));
       pictureAddLabel=insertText(pictureAddLabel,[row-5,position-150],num2str(position-150));
       pictureAddLabel=insertText(pictureAddLabel,[row-5,position-300],num2str(position-300));
    end
else
     pictureAddLabel=insertText(pictureAddLabel,[301,row-25],num2str(position));
     pictureAddLabel=insertText(pictureAddLabel,[451,row-25],num2str(position+150));
     pictureAddLabel=insertText(pictureAddLabel,[151,row-25],num2str(position-150));
     imshow(pictureAddLabel);
end