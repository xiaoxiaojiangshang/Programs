% clear all;
for K=1:2
    b=num2str(K)
    FileName=[b];
    load(FileName)
    a=IPD.d;
    a_std=std(a);
    a_std=a_std(:);
    std_size=size(a_std);
    std_mean=mean(a_std);
    t=0:std_size(1)-1;
    Lmax = diff(sign(diff(a_std)))== -2; % logic vector for the local max value
    Lmax;
    Lmin = diff(sign(diff(a_std)))== 2; % logic vector for the local min value
    % match the logic vector to the original vecor to have the same length
    Lmax = [false; Lmax; false];
    Lmin =  [false; Lmin; false];

    tmax = t (Lmax); % locations of the local max elements
    tmin = t (Lmin); % locations of the local min elements
    tmin(end)=[];
    vmax = a_std(Lmax); % values of the local max elements
    vmin = a_std(Lmin); % values of the local min elements
    
    tmax=tmax(:);
    tmin=tmin(:);
    list=[tmax;tmin];
    list=reshape(list,[],1);
    list=sort(list);
    cad_point=[];
    for i=1:size(list)-1
        if(mean(a_std(list(i):list(i+1)))>std_mean*2)
            cad_point=[cad_point,list(i),list(i+1)];
        end
    end
    if (size(cad_point))
        i=1;
        while(cad_point(i)~=cad_point(end))
            if(cad_point(i)==cad_point(i+1))
                cad_point(i)=[];
                cad_point(i)=[];
            else i=i+1;
            end
        end
        size_cad=size(cad_point(:));
%         size_cad=size_cad(2);
            for j=1:335
                for i=1:size_cad
                for k=cad_point(i)-5:cad_point(i)+5
                    a(j,k)=max(max(a));
                end
            end
            end
              figure;imshow(a,[]);
    else fprintf('No found')
    end
    eval(['cad_point',num2str(K),'=','cad_point',';'])
end
