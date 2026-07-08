clc;
clear;
close all;
%% 附件1 数据处理
% 指定CSV 文件路径和文件名
filename = '附件1.csv';
% 使用readtable 函数读取CSV 文件,包括变量名
data = readtable(filename, 'ReadVariableNames', true);
% 分拣中心列表
centers = unique(data{:, 1}); % 提取唯一的分拣中心名称
% 按分拣中心分组数据,并对每组数据按日期排序
sortedData1 = cell(length(centers), 1); % 创建单元格数组存放排序后数据
for i = 1:length(centers)
    centerData = data(strcmp(data{:, 1}, centers{i}), :); % 筛选出当前分拣中心的数据
    sortedData1{i} = sortrows(centerData, 2); % 按日期排序该分拣中心的数据
end
% 保存处理后的数据到MAT 文件,方便后续使用
save('data1.mat', 'sortedData1');

%% 附件2 数据处理
% 指定CSV 文件路径和文件名
filename = '附件2.csv';
% 使用readtable 函数读取CSV 文件
data = readtable(filename);
% 获取唯一的分拣中心列表
centers = unique(data{:, 1});
% 创建单元格数组存放每个分拣中心排序后的数据
sortedData2 = cell(length(centers), 1);
for i = 1:length(centers)
    centerData = data(strcmp(data{:, 1}, centers{i}), :); % 筛选当前分拣中心的数据
    sortedData2{i} = sortrows(centerData, [2, 3]); % 按日期和小时排序
end
% 对于每个分拣中心的数据进行缺失小时数据的填充
for k = 1:57
    if size(sortedData2{k}, 1) <= 720
        % 确保每天24小时的数据都完整
        if table2array(sortedData2{k}(end, 3)) == 23
            p = 0;
            for i = 1:30
                for j = 1:24
                    % 检查是否存在缺失的小时数据,并进行插入
                    if table2array(sortedData2{k}(j+p, 3)) ~= j - 1
                        insert_name = sortedData2{k}(1, 1);
                        insert_date = sortedData2{k}(j+p+2, 2);
                        % 创建要插入的新行
                        newRow = [insert_name, insert_date, table(j-1, 0, 'VariableNames',{'hour', 'm'})];
                        % 插入新行
                        sortedData2{k} = [sortedData2{k}(1:j+p-1, :); newRow; sortedData2{k}(j+p:end, :)];
                    end
                end
                p = p + 24;
            end
        else
            %处理不完整的天数,确保每天结束时为23时
            while table2array(sortedData2{k}(end, 3)) ~= 23
                pos = table2array(sortedData2{k}(end, 3)) + 1;
                insert_name = sortedData2{k}(1, 1);
                insert_date = sortedData2{k}(end, 2);
                newRow = [insert_name, insert_date, table(pos, 0,'VariableNames',{'hour','m'})];
                sortedData2{k} = [sortedData2{k}; newRow];
            end
            p = 0;
            for i = 1:30
                for j = 1:24
                    if table2array(sortedData2{k}(j+p, 3)) ~= j - 1
                        insert_name = sortedData2{k}(1, 1);
                        insert_date = sortedData2{k}(j+p+2, 2);
                        newRow = [insert_name, insert_date, table(j-1, 0,'VariableNames',{'hour','m'})];
                        sortedData2{k} = [sortedData2{k}(1:j+p-1, :); newRow; sortedData2{k}(j+p:end, :)];
                    end
                end
                p = p + 24;
            end
        end
    end
end
% 保存处理后的数据到MAT文件
save('data2.mat','sortedData2');
