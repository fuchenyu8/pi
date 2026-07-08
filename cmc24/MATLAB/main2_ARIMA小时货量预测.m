clc
clear
close all

% 加载数据
load data2

%% 数据预处理和建模
result = []; % 存储预测结果
data = []; % 存储原始数据

% 提取每个数据集的第四列作为分析数据
for i = 1:57
    data(:,i) = table2array(sortedData2{i}(:,4));
end

% 对每个数据集进行ARIMA 模型拟合和预测
for j = 1:57
    % 导入数据
    y = data(:,j);

    % 创建ARIMA 模型
    Mdl = arima(24,0,0); % 使用24 小时滞后作为自回归项

    % 拟合模型
    EstMdl = estimate(Mdl, y);

    % 预测未来720 期数据
    numPeriods = 720;
    [YF, YMSE] = forecast(EstMdl, numPeriods, 'Y0', y);

    % 将预测结果存储到结果矩阵中
    result(:,j) = YF;
end

%% 修正负值并绘图
% 绘制前30 列数据的图表
figure;
for i = 1:30
    subplot(6, 5, i);
    % 绘制原始数据
    plot(data(1:end,i), 'm')
    hold on
    idx = 721:(720+720);
    % 绘制预测结果
    plot(idx, result(:,i), '.-', 'Color', [0.8500, 0.3250, 0.0980])
    hold off
    xlabel("货量")
    ylabel("时间")
    legend(["观测值" "预测值"])
end

% 绘制后27 列数据的图表
figure;
for i = 31:57
    subplot(6, 5, i-30);
    % 绘制原始数据
    plot(data(1:end,i))
    hold on
    idx = 721:(720+720);
    % 绘制预测结果
    plot(idx, result(:,i), '.-', 'Color', [0.8500, 0.3250, 0.0980])
    hold off
    xlabel("货量")
    ylabel("时间")
    legend(["观测值" "预测值"])
end

%% 将结果保存到CSV 文件
% 初始化存储各项数据的变量
center_write = [];
date_write = [];
result_write = [];
hour_write = [];

% 指定要保存的CSV 文件名
filename = '结果表2.csv';

% 生成时间数据
startDate = datetime(2023, 12, 1);
endDate = datetime(2023, 12, 30);
timeData = startDate:endDate;

% 将时间数据转换为字符串格式
timeString = datestr(timeData, 'yyyy/mm/dd');
date = cellstr(timeString);

% 扩展日期并生成小时数据
expanded_date = {};
for i = 1:numel(date)
    repeated_date = cellstr(repmat(date{i}, 24, 1));
    expanded_date = [expanded_date; repeated_date];
end

% 生成小时数据
for i = 1:30
    hour_write = [hour_write; (0:23)'];
end

% 重复日期和小时数据以匹配结果数据
date_write = [];
for k = 1:57
    date_write = [date_write; expanded_date];
end

hour_write1 = [];
for k = 1:57
    hour_write1 = [hour_write1; hour_write];
end

% 将结果数据和其他相关数据存储到相应变量中
for k = 1:57
    center = sortedData2{k}(1:720,1);
    center = table2cell(center);
    center_write = [center_write; center];
    result_write = [result_write; result(:,k)];
end

% 将数据写入CSV 文件
xlswrite(filename, [center_write, date_write, num2cell(hour_write1), num2cell(result_write)], '结果表2', 'A2');
