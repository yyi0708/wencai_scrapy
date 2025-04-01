# 数据爬虫说明文档

## 项目简介

本项目旨在通过爬虫技术从目标网站获取数据，并对数据进行清洗和存储，以便后续分析和使用。

## 环境依赖

请确保您的环境满足以下要求：

- Python 版本 >= 3.8
- 必要的依赖库：
  - `appwrite`
  - `Scrapy`
  - `python-dotenv`

安装依赖：

```bash
pip install -r requirements.txt
```

## 文件结构

```
wencai_scapy/
├── README.md          # 项目说明文档
├── requirements.txt   # 依赖库列表
├── main.py            # 主程序入口
├── utils/             # 工具函数目录
│   ├── parser.py      # HTML 解析工具
│   └── storage.py     # 数据存储工具
└── data/              # 数据存储目录
```

## 使用说明

1. **配置目标网站和参数**  
    在 `main.py` 中设置目标网站的 URL 和爬取参数。

2. **运行爬虫**  
    执行以下命令启动爬虫：

   ```bash
   python main.py
   ```

3. **查看结果**  
    爬取的数据将存储在 `data/` 目录下，格式为 CSV 文件。

## 注意事项

- 请遵守目标网站的 `robots.txt` 文件和相关法律法规。
- 爬取频率不宜过高，以避免对目标网站造成压力。

## 常见问题

1. **如何处理反爬机制？**  
    可以尝试使用代理池或模拟浏览器请求（如 `selenium`）。

2. **数据格式不一致怎么办？**  
    使用 `pandas` 对数据进行清洗和格式化。

## 联系方式

如有问题，请联系开发者：`yangyi@example.com`
