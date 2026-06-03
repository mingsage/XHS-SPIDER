# 小红书数据爬虫

基于 Scrapy 框架的小红书数据采集系统，支持图文/视频笔记元数据抓取，MongoDB 存储 + 视频文件下载。

## 功能

- ✅ 推荐页笔记抓取（去重）
- ✅ 自动识别图文 / 视频类型
- ✅ 标题、作者、发布时间、点赞、收藏、评论数等元数据
- ✅ 视频自动下载到本地
- ✅ MongoDB 持久化存储
- ✅ 随机请求延迟（1~3 秒）

## 环境要求

- Python 3.8+
- MongoDB 5.0+

## 安装

### pip（原生）

```bash
pip install -r requirements.txt
```

### uv（推荐）

```bash
uv sync
```

## 配置

确保本机 MongoDB 已启动，然后在 [redbook/settings.py](redbook/settings.py) 中确认连接信息与你的环境一致：

```python
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'redbook'
```
默认是一致的，只要 MongoDB 服务在运行，启动项目后会自动创建 redbook 的数据库。

视频默认存储路径为项目根目录下的 `database/videos/`，可在 `settings.py` 中修改 `VIDEO_STORE_PATH`。

## 快速开始

```bash
# pip 用户
python run_spider.py

# uv 用户
uv run python run_spider.py # 或者激活虚拟环境后采取 python run_spider.py
```

爬虫会循环运行，直到抓满 **5000 条笔记 + 50 个视频**后自动停止。你也可以按 `Ctrl+C` 随时中断。

## 项目结构

```
XHS-SPIDER/
├── run_spider.py           # 入口脚本（循环启动 + 进度统计）
├── requirements.txt        # pip 依赖
├── pyproject.toml          # 项目配置 / uv 依赖
├── scrapy.cfg              # Scrapy 部署配置
├── redbook/                # Scrapy 项目包
│   ├── spiders/
│   │   └── xhs.py          # 核心爬虫（推荐页 → 详情页）
│   ├── items.py            # 数据模型（RedbookItem / CommentItem）
│   ├── pipelines.py        # MongoDB 存储管道
│   ├── middlewares.py      # 下载中间件
│   ├── settings.py         # 全局配置（MongoDB / UA / 路径）
│   └── videodownloader.py  # 视频下载工具
├── samples/                # 页面 HTML 样本（开发调试用）
└── database/
    └── videos/             # 已下载的视频文件
```

## 数据示例

MongoDB `redbook.notes` 集合中的一条记录：

```json
{
  "type": "video",
  "title": "汉服在国外（炸街系列）",
  "author": "周宝不保周",
  "time": ["2023-07-03"],
  "note_link": "https://www.xiaohongshu.com/explore/64a26705000000001c00fd8d",
  "author_link": "https://www.xiaohongshu.com/explore/64a26705000000001c00fd8d",
  "like_count": "7.5万",
  "comment_count": "1403",
  "collect_count": "8111",
  "keywords": "",
  "description": "让世界看到中国旗袍～",
  "media_url": "https://sns-video-qc.xhscdn.com/stream/..."
}
```

## 已知限制

- 图文笔记的多图列表为 JS 动态加载，纯 Scrapy 无法获取
- 评论抓取接口已预留（`CommentItem`），尚未实现
- 无代理池 / Cookie 管理，高频率抓取可能触发反爬
- XPath 表达式依赖页面结构，小红书改版可能导致失效
- **爬取笔记多为旧内容（如 2023 年）**：探索页为 SPA 单页应用，笔记列表由 JS 动态渲染。Scrapy 只能获取原始 HTML，无法执行 JS，拿到的实际是页面中给 SEO 准备的静态兜底内容，这些兜底数据通常是较老的高互动量笔记，基本不更新。解决方向：换用 Playwright/Selenium 等可执行 JS 的工具，或直接抓包调用后端 API 获取 JSON 数据

## 注意事项

1. 爬虫默认忽略 `robots.txt`（`ROBOTSTXT_OBEY = False`），请合理使用
2. 请勿将抓取数据用于商业用途，遵守相关法律法规
