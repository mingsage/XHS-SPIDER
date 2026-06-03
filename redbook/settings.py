BOT_NAME = "redbook"
SPIDER_MODULES = ["redbook.spiders"]
NEWSPIDER_MODULE = "redbook.spiders"
ADDONS = {}
FEED_EXPORT_ENCODING = "utf-8"
# MongoDB配置
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'redbook'
# 启用管道
ITEM_PIPELINES = {
    'redbook.pipelines.MongoDBPipeline': 300, 
}
# 添加自定义请求头
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}
# 关闭robots.txt检查
ROBOTSTXT_OBEY = False
# 项目根目录（settings.py 在 redbook/ 下，往上两级是项目根）
import os
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 添加视频存储配置（项目根目录下的 database/videos/）
VIDEO_STORE_PATH = os.path.join(_PROJECT_ROOT, 'database', 'videos')
# 创建视频存储目录（如果不存在）
if not os.path.exists(VIDEO_STORE_PATH):
    os.makedirs(VIDEO_STORE_PATH)
