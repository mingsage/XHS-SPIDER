import os
import pymongo
import glob
from datetime import datetime

# 项目根目录（run_spider.py 所在目录）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 连接MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['redbook']
collection = db['notes']

# 获取并打印数据库记录数
def print_db_count():
    count = collection.count_documents({})  # 获取总记录数
    print(f"当前数据库记录数: {count}")
    return count

# 获取并打印视频文件数
def print_video_count():
    video_dir = os.path.join(BASE_DIR, 'redbook', 'database', 'videos')
    video_count = len(glob.glob(video_dir + '/*.mp4'))  # 统计mp4文件数量
    print(f"当前视频文件数: {video_count}")
    return video_count

def write_to_file(db_count, video_count):
    """
    将数据统计写入文件
    :param db_count: 数据库记录数
    :param video_count: 视频文件数
    """
    try:
        # 指定完整文件路径
        file_path = os.path.join(BASE_DIR, 'redbook', 'database', '爬虫数据清单.txt')
        
        # 获取当前时间
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 写入文件(追加模式，UTF-8编码)
        with open(file_path, 'a', encoding='utf-8') as f:
            # 格式化输出：时间 | 数据数量 | 视频数量
            f.write(f"{timestamp} | {db_count} | {video_count}\n")
            
        print(f"数据已成功写入: {file_path}")
        
    except Exception as e:
        print(f"写入文件时出错: {e}")

# 主循环
while True:
    os.system("scrapy crawl xhs")  # 运行爬虫
    
    # 打印当前数据统计
    db_count = print_db_count()
    video_count = print_video_count()

    write_to_file(db_count, video_count)
    
    # 检查条件
    if db_count >= 5000 and video_count >= 50:
        print("已达到数据收集目标，停止爬虫")
        break
