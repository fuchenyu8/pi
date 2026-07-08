clc
clear
close all
load data1 %加载数据文件

% 初始化结果数组
result = [];
data = [];

% 提取数据列并进行预处理
for i = 1:57
    data(:,i) = table2array(sortedData1{i}(:,3)); % 提取第三列数据并存储
end

for j = 1:57
    % 定义训练集和测试集
    dataTrain = data(1:100,j)'; % 用前100 个数据作为训练集
    dataTest = data(101:122,j)'; % 后面的数据作为测试集

    % 数据标准化
    mu = mean(dataTrain);
    sig = std(dataTrain);
    dataTrainStandardized = (dataTrain - mu) / sig;

    % 准备训练数据
    XTrain = dataTrainStandardized(1:end-1);
    YTrain = dataTrainStandardized(2:end);

    % 创建 LSTM 网络模型
    numFeatures = 1;
    numResponses = 1;
    numHiddenUnits = 100;
    layers = [ ...
        sequenceInputLayer(numFeatures)
        lstmLayer(numHiddenUnits)
        fullyConnectedLayer(numResponses)
        regressionLayer];

    % 训练网络
    options = trainingOptions('adam', ...
        'MaxEpochs', 300, ...
        'GradientThreshold', 1, ...
        'InitialLearnRate', 0.01, ...
        'LearnRateSchedule', 'piecewise', ...
        'LearnRateDropPeriod', 400, ...
        'LearnRateDropFactor', 0.15, ...
        'Verbose', 0);
    net = trainNetwork(XTrain, YTrain, layers, options);

    % 进行预测
    net = predictAndUpdateState(net, XTrain);
    [net, YPred] = predictAndUpdateState(net, YTrain(end));
    for i = 2:52
        [net, YPred(:,i)] = predictAndUpdateState(net, YPred(:,i-1), 'ExecutionEnvironment', 'cpu');
    end

    % 验证网络
    YPred1 = sig * YPred + mu;
    rmse = sqrt(mean((YPred1(1:22) - dataTest).^2)); % 计算均方根误差
    result(:,j) = YPred1(23:end)';
end

% 绘制图表
figure;
for i = 1:30
    subplot(5, 6, i);
    plot(data(1:end,i), 'color', [0.5, 0, 0.5]) % 绘制观察值
    hold on
    idx = 123:(122+30);
    plot(idx, result(:,i), '.-', 'color', [1, 0.5, 0]) % 绘制预测值
    hold off
    xlabel("时间") % x 轴标签
    ylabel("货量") % y 轴标签
    legend(["观察值" "预测值"]) % 添加图例
end

figure;
for i = 31:57
    subplot(5, 6, i-30);
    plot(data(1:end,i), 'color', [0.5, 0, 0.5]) % 绘制观察值
    hold on
    idx = 123:(122+30);
    plot(idx, result(:,i), '.-', 'color', [1, 0.5, 0]) % 绘制预测值
    hold off
    xlabel("时间") % x 轴标签
    ylabel("货量") % y 轴标签
    legend(["观察值" "预测值"]) % 添加图例
end

% 准备要写入 Excel 文件的数据
center_write = [];
date_write = [];
result_write = [];
filename = '结果表1.csv';
variable_names = {'分拣中心', '日期', '货量'};
writecell(variable_names, filename);
startDate = datetime(2023, 12, 1);
endDate = datetime(2023, 12, 30);
timeData = startDate:endDate;
timeString = datestr(timeData, 'yyyy/mm/dd');
date = cellstr(timeString);

% 将数据写入 Excel 文件
for k = 1:57
    center = sortedData1{k}(1:30,1);
    center = table2cell(center);
    center_write = [center_write; center];
    date_write = [date_write; date];
    result_write = [result_write; result(:,k)];
end
xlswrite(filename, [center_write, date_write, num2cell(result_write)], '结果表1', 'A2');
