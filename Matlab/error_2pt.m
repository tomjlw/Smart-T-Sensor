close all ; clc; 
file = readmatrix("foo.csv");
CONST_TK = (283:5:323)'; 
CONST_TK = [273;277;CONST_TK];
CONST_TK = (273:20:373)';
TK = CONST_TK;
temp=TK;
% pt1_val = temp(2,:);
% pt2_val = temp(17,:);
%data_Nominal=file.Nominal; % data is frequency
% data_FF=file.FF; 
% data_SS=file.SS;
% data_SF=file.SF;
% data_FS=file.FS;
% data_TT=file.TT;
coefficients = [];
mode="Yang";
%data = str2double([data_Nominal data_TT data_FF data_FS data_SF data_SS]);
%data = [data_TT data_FF data_FS data_SF data_SS];%data=data;
data = file(1:6,:);
marker = ["-ro", "-b+", "-gs", "-cd", "-m*", "-kh"];
marker2 = ["--r+", "--bo", "--gd", "--cs", "--mh", "--k*"];
close all;
Samples=size(data, 2); %number of chips
temp_number=size(data, 1); %number of temperatures
error=zeros(temp_number,Samples);
error_2pt=zeros(temp_number,Samples);
temp = repmat(TK,1,Samples);
c = [];
for i=1:Samples
    if strcmp(mode, 'Yang')
        Process=temp(:,i).*log(data(:,i));
        %c_new = log(data(:,i));
        c = [c,Process];
    else
        Process=data(:,i);
    end    
    %linear regression    
    P=polyfit(temp(:,i),Process,1);
    Meas=P(2)./(log(data(:,i))-P(1));
    error(:,i)=Meas-temp(:,i);
    
    %2 point calibration
    P=polyfit([temp(3,i);temp(6,i)],[Process(3);Process(6)],1); % create a curve that passes chosen 2 pt 
%   P=polyfit([temp(5,i)],[Process(5)],1); % create a curve that passes chosen 2 pt 
    Meas=P(2)./(log(data(:,i))-P(1)); % calculated T
    error_2pt(:,i)=Meas-temp(:,i);
end
% 
figure
plot(temp(:,1)-273,c, "*--");

%% plotting linear regresssion results
figure
plot(temp(:,1)-273, data, "r*--");

figure;
plot(temp(:,1)-273, error);
hold on;
FF=polyfit(temp,error,3);
plot(temp(:,1)-273,polyval(FF,temp(:,1)),'r*--');


%After lot based calibration
error_after_fitting=(error-polyval(FF,temp));

figure;
plot(temp(:,1)-273, error_after_fitting,"s-")
sigma=std(error_after_fitting,0,2);
average=mean(error_after_fitting,2);
hold on;
plot(temp(:,1)-273,average+3*sigma,'r*--');
plot(temp(:,1)-273,average-3*sigma,'r*--');
max(average+3*sigma)
min(average-3*sigma)
title("Linear Regression Accuracy");
%legend(["TT", "FF", "FS", "SF", "SS"], "FontSize", 5, "Location","best");
%% plotting 2 point calibration results

figure;
plot(temp, error_2pt);
hold on;
FF=polyfit(temp,error_2pt,3);
plot(temp,polyval(FF,temp(:,1)),'r*');
 
%After lot based calibration
error_2pt_after_fitting=error_2pt-polyval(FF,temp);

figure;
plot(temp(:,1)-273, error_2pt_after_fitting, "s-")
sigma=std(error_2pt_after_fitting,0,2);
average=mean(error_2pt_after_fitting,2);
hold on;
plot(temp(:,1)-273,average,'r*--');
writematrix(c,'0_100_R2.csv');
%plot(temp(:,1)-273,average-3*sigma,'r*--');
sigma_max=max(average+3*sigma)
sigma_min=min(average-3*sigma)
title("2pt Caliberation Accuracy");
%legend(["TT", "FF", "FS", "SF", "SS"], "FontSize", 5, "Location","best");
