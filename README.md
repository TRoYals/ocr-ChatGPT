# About the Project

Use baidu OCR Form api and ChatGPT api to extract FORM from the PDF.

A sample project to serve as the first step to data anylsis.

# How to use?

1. text your ocr api and ChatGPT api in the config.ini
2. put your pdf in the user_file folder.
3. adjust your needed prompt in the config.ini
4. simply run the src/main.py and you can see all the temp form in the temp folder and display form in the output folder.

# 项目状态

2023-05-30 10:34 基本满足最小实现要求, 确认需求后再继续改进

2023-06-01 15:44 基本完成了，满足 zoe 的需求，但 ocr 识别上存在的问题还是蛮明显的，考虑要不要换 ocr 识别。

# Todo

- [ ] 单元测试
- [ ] GPT prompt engeering
- [ ] 使用表格+文本识别时, 文本内容可能过长, 需要对内容进行简单的分割
- [x] 文本识别时,返回的内容空格较多, 可能会对 ChatGPT 调用产生影响
- [ ] GPT4 支持
- [ ] 其他 ocr 支持
- [ ] 百度表格 高精度 v2 支持?
- [x] 表格合并指定内容?
- [x] 文本内容数据转换?
- [x] 多 pdf 处理
- [x] pdf 文件名抓取
- [ ] 数据验证
