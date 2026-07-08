clc;
clear;
close all;

%% 从CSV 文件读取数据
data1 = readtable('附件3.csv'); % 读取第一个CSV 文件中的数据
startnote1 = data1{:,1}; % 提取第一个文件中的起始节点
endnote1 = data1{:,2}; % 提取第一个文件中的结束节点
m1 = data1{:,3}; % 提取第一个文件中的权重

data2 = readtable('附件4.csv'); % 读取第二个CSV 文件中的数据
startnote2 = data2{:,1}; % 提取第二个文件中的起始节点
endnote2 = data2{:,2}; % 提取第二个文件中的结束节点

%% 匹配和计算结果
k = []; % 初始化空数组以跟踪匹配的索引
result = zeros(122,1); % 使用零初始化结果数组
for i = 1:122
    for j = 1:134
        if (isequal(startnote1{j}, startnote2{i}) && isequal(endnote1{j}, endnote2{i}))
            result(i) = m1(j); % 在节点匹配时分配权重
            k = [k; j]; % 收集匹配节点的索引
        end
    end
end
k = sort(k); % 对匹配节点的索引进行排序
notInK = setdiff(1:134, k); % 查找未匹配的索引

%% 根据不同分拣中心提供的公式调整权重
% SC8 调整
w = [240, 75, 296, 139, 147, 213, 103, 257, 205, 72, 104, 54, 172];
w_new = (w ./ 2077 * 97) + w;

% SC15 调整
w = [176, 67, 16, 38, 245];
w_new = (w ./ 542 * 369) + w;

% SC47 调整
w = [211, 68, 340, 146, 150, 234, 134, 43, 351, 209, 62, 104, 84, 203, 70, 240, 180];
w_new = (w ./ 2829 * 133) + w;

% SC7 调整
w = [85, 204, 142, 139, 222, 62, 35, 225, 234, 79, 99, 171, 30, 167];
w_new = (w ./ 1894 * 128) + w;

% SC5 调整
w = [117, 64, 122, 145, 188, 41, 173, 69, 96, 146, 22];
w_new = (w ./ 1183 * 138) + w;

% SC51 调整
w = [55, 36, 68, 49, 50];
w_new = (w ./ 258 * 14) + w;

% SC25 调整
w = [76, 176, 115, 129, 207, 196];
w_new = (w ./ 899 * 436) + w;

% SC10 调整
w = [78, 78, 85, 123];
w_new = (w ./ 364 * 228) + w;
w_new

% SC60 调整
w = [111, 36, 431];
w_new = (w ./ 578 * 119) + w;

%% 清空工作区并加载必要的数据
clc; % 清空命令窗口
clear; % 清空工作区
close all; % 关闭所有图形窗口
load rate; % 加载费率数据
load result1; % 加载结果1 数据
load data1; % 加载数据1 数据

% 为每个分拣中心提取第一个排序中心的名称
for i = 1:57
    column(:,i) = table2array(sortedData1{i}(1,1)); % 提取分拣中心名称
end
name = cellstr(name); % 将名称转换为单元字符串

% 根据费率调整结果1
for i = 1:11
    for j = 1:57
        if isequal(column{j}, name{i})
            result(:,j) = (1 + rate(i)) .* result(:,j); % 根据费率调整结果
        end
    end
end

% 初始化用于写入Excel 的数组
center_write = [];
date_write = [];
result_write = [];

% 指定Excel 文件名
filename = '结果表3.csv';

% 将变量名称写入Excel 文件的第一列
variable_names = {'分拣中心','日期','货量'};
writecell(variable_names, filename);

% 定义开始和结束日期
startDate = datetime(2023, 12, 1);
endDate = datetime(2023, 12, 30);

% 生成时间数据
timeData = startDate:endDate;

% 将日期时间数据转换为指定格式的字符串
timeString = datestr(timeData, 'yyyy/mm/dd');
date = cellstr(timeString); % 将日期转换为单元字符串

for k = 1:57
    center = sortedData1{k}(1:30,1); % 提取中心数据
    center = table2cell(center); % 将表格转换为单元格
    center_write = [center_write; center]; % 收集中心数据
    date_write = [date_write; date]; % 收集日期数据
    result_write = [result_write; result(:,k)]; % 收集结果数据
end

% 写入数据到Excel 文件的第一列,从A2 开始追加数据
xlswrite(filename, [center_write, date_write, num2cell(result_write)], '结果表3', 'A2');

%% 清空工作区并加载必要的数据
clc; % 清空命令窗口
clear; % 清空工作区
close all; % 关闭所有图形窗口
load rate; % 加载费率数据
load result2; % 加载结果2 数据
load data2; % 加载数据2

% 为每个分拣中心提取第二个排序中心的名称
for i = 1:57
    column(:,i) = table2array(sortedData2{i}(1,1)); % 提取分拣中心名称
end
name = cellstr(name); % 将名称转换为单元字符串

% 根据费率调整结果2
for i = 1:11
    for j = 1:57
        if isequal(column{j}, name{i})
            result(:,j) = (1 + rate(i)) .* result(:,j); % 根据费率调整结果
        end
    end
end

% 初始化用于写入Excel 的数组
center_write = [];
date_write = [];
result_write = [];
hour_write = [];

% 指定Excel 文件名
filename = '结果表4.csv';

% 将变量名称写入Excel 文件的第一列
variable_names = {'分拣中心','日期','小时','货量'};
writecell(variable_names, filename);

% 定义开始和结束日期
startDate = datetime(2023, 12, 1);
endDate = datetime(2023, 12, 30);

% 生成时间数据
timeData = startDate:endDate;

% 将时间数据转换为字符串格式
timeString = datestr(timeData, 'yyyy/mm/dd');
date = cellstr(timeString); % 将日期转换为单元字符串

% 初始化一个空数组来存储扩展后的日期
expanded_date = {};

% 循环遍历每个日期
for i = 1:30
    hour_write = [hour_write; (0:23)']; % 生成小时数据
end

% 循环遍历每个日期
for i = 1:numel(date)
    % 将当前日期重复24 次
    repeated_date = cellstr(repmat(date{i}, 24, 1));
    % 将重复后的日期追加到数组中
    expanded_date = [expanded_date; repeated_date];
end

date_write = [];
for k = 1:57
    date_write = [date_write; expanded_date]; % 收集日期数据
end

hour_write1 = [];
for k = 1:57
    hour_write1 = [hour_write1; hour_write]; % 收集小时数据
end

for k = 1:57
    center = sortedData2{k}(1:720,1); % 提取中心数据
    center = table2cell(center); % 将表格转换为单元格
    center_write = [center_write; center]; % 收集中心数据
    result_write = [result_write; result(:,k)]; % 收集结果数据
end

% 写入数据到Excel 文件的第一列,从A2 开始追加数据
xlswrite(filename, [center_write, date_write, num2cell(hour_write1), num2cell(result_write)], '结果表4', 'A2');
