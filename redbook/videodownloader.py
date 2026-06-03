import requests
import os
import time
import random

def download_video(video_url, save_path=None):
    """
    下载视频并保存到指定路径
    :param video_url: 视频URL
    :param save_path: 保存路径，如果为None则自动生成
    """
    if not save_path:
        # 自动生成文件名，使用时间戳+随机数
        filename = f"video_{int(time.time())}_{random.randint(1000,9999)}.mp4"
        save_path = os.path.join('database', 'videos', filename)
    
    # 确保videos目录存在
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    if video_url:
        try:
            response = requests.get(video_url)
            response.raise_for_status()  # 检查请求是否成功
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"视频已成功保存到: {save_path}")
            return True
        except Exception as e:
            print(f"下载视频失败: {e}")
            return False
    else:
        print("视频URL为空")
        return False

# 示例调用
if __name__ == "__main__":
    video_url = 'https://sns-video-qc.xhscdn.com/stream/79/110/258/01e862559c1739c04f03700197c01f0612_258.mp4?sign=df27cb80588e9a1c13d2cdbe5b20db17&t=68692fad'
    download_video(video_url)