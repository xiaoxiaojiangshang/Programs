function detectFile(dirName)
period = 10; %seconds between directory checks
timeout = 50; %seconds before function termination
dirLength = length(dir(dirName));
 fileFolder=fullfile(dirName);
 dirOutput=dir(fullfile(fileFolder,'*'));
 fileName={dirOutput.name}';
t = timer('TimerFcn', {@timerCallback, dirName, dirLength,fileName}, 'Period', period,'TaskstoExecute', uint8(timeout/period), 'executionmode', 'fixedrate');
start(t)

