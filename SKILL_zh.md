# PDF 施工/养护日志审计 Skill（中文说明）

## 功能概述

该 Skill 用于批量审计工程日志、养护日志、施工日志、巡检日志等 PDF 文件，并为每个 PDF 生成一个对应的 Word 分析报告。

核心能力：
- 扫描单个 PDF 或整个目录下的 PDF
- 提取 PDF 内嵌图片
- 过滤页眉、页脚、模板类小图，避免误判
- 检测重复施工照片
- 检测明确的图文不符问题
- 当前稳定支持的明确问题：**日期与星期不一致**
- 为每个 PDF 在原目录下生成一个 `分析报告.docx`
- 支持随机抽查复核

---

## 当前适用场景

适合以下类型文档：
- 工程日志
- 养护日志
- 施工日志
- 巡检日志
- 园林、绿化、市政类项目 PDF 台账

---

## 判定原则

该 Skill 采用**保守判定策略**，只输出能够明确坐实的问题。

### 会输出的问题
- 重复图片
- 日期与星期不一致

### 默认不会输出的问题
以下问题如果没有非常明确的证据，不会默认输出：
- 季节可能不符
- 天气可能不符
- 施工内容可能不符
- 仅凭经验怀疑但无法坐实的问题

例如：
- “感觉像夏天，不像冬天” → 默认不报
- “可能不是当天施工图” → 默认不报
- “图片看起来和文字不太像” → 默认不报

---

## 报告格式

每份报告只保留两个章节：

1. `重复图片问题`
2. `明确的图文不符问题`

规则：
- 同一组重复图片只写一行
- 不拆成多条描述
- 如果某一类问题不存在，就写“未发现”
- 默认不写建议
- 默认不写图片分析详情
- 默认不写疑似风险项

---

## 图片过滤规则

为了避免把 PDF 模板图、页眉图、页脚图误判为施工照片，默认会过滤较小的图片。

默认阈值：
- 宽度 >= 500
- 高度 >= 350
- 图片字节数 >= 50000

如果某些 PDF 版式特殊，可以调整阈值，但不要轻易关闭过滤。

---

## 使用脚本

脚本位置：

`./scripts/analyze_pdf_site_logs.py`

### 处理单个 PDF

```bash
python3 scripts/analyze_pdf_site_logs.py "/path/to/file.pdf"
```

### 递归处理整个目录

```bash
python3 scripts/analyze_pdf_site_logs.py "/path/to/folder" --recursive
```

### 自定义过滤阈值

```bash
python3 scripts/analyze_pdf_site_logs.py "/path/to/folder" --recursive \
  --min-width 500 --min-height 350 --min-bytes 50000
```

### 导出 JSON 汇总结果

```bash
python3 scripts/analyze_pdf_site_logs.py "/path/to/folder" --recursive \
  --json-out /tmp/pdf_audit_summary.json
```

### 启用随机抽查复核

```bash
python3 scripts/analyze_pdf_site_logs.py "/path/to/folder" --recursive \
  --sample-check 5 --json-out /tmp/pdf_audit_summary.json
```

---

## 输出结果

执行后会产生两类输出：

1. 每个 PDF 同目录下生成一个 Word 报告
   - 文件名格式：原文件名 + ` 分析报告.docx`

2. 标准输出 / JSON 汇总
   - 包含每个 PDF 的问题统计
   - 如果启用抽查，会附带 `sample_checks`

---

## 出现异常结果时如何排查

如果报告显示“大量页面使用同一张图片”，优先怀疑以下情况：
- PDF 中存在重复页眉图
- PDF 中存在固定模板图片
- 图片过滤阈值过低

建议优先检查：
- 重复图片尺寸是否很小
- 是否呈现横幅、页眉、页脚形态
- 调高阈值后重新运行

---

## 推荐复核方式

当结果需要更高可信度时，建议：
- 批处理后随机抽查 3-5 份 PDF
- 重点查看有重复图片的报告
- 重点查看有日期错误的报告
- 如需更深层的季节/天气/施工内容核查，应作为第二轮人工复核，而不是默认批量输出的一部分
