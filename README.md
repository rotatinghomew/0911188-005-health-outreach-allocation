# 公益医疗服务概览

服务点、物资批次和诊疗或培训记录。当前总览只按服务点统计记录人数。

样例数据均为本地合成记录，不对应真实个人、媒体、机构或交易。项目使用 Python 3.11.14 标准库，数据随项目保存，不访问外部服务。

## 使用

在项目根目录运行 `python3 -m app summary` 查看按当前基础口径生成的 JSON 总览。

## 验证

运行 `python3 -m unittest discover -s tests -v` 和 `python3 -m compileall -q app tests`。

## 结构

`data/data.json` 保存领域记录与基础汇总口径；`app/storage.py` 读取并检查数据形状；`app/analysis.py` 计算基础分组统计；`app/service.py` 组合数据读取和统计；`tests/` 验证产品入口及无效数据处理。

## 工作台

现在每站按截至日期已报的服务完成记录报数，物资按批次扣实际发放，下一轮在保护已有预留后按完成数优先提议余量。用 `python3 -m app coverage`、`python3 -m app stock` 和 `python3 -m app allocation` 查看这三份资料。

`person` 是合成服务对象编号，区别于每次接触的 `id`；同一个对象的转介通过 `initial` 和 `outcome` 连接。站点报数进度为 `period_reports_through`，不等同于一条记录的 `reported`。物资发放单的 `contact` 用于核对实物去向。培训签到不发基本物资包；站点预留和发放是两回事。

操作数据在 `data/workbench.json`。工作台涉及的领域代码：`coverage` 生成站点完成数, `inventory` 对物资批次核库存, `allocation` 预留下一轮物资。已有总览仍使用 `data/data.json`。
