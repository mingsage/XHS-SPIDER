import scrapy
from ..items import RedbookItem
from ..settings import VIDEO_STORE_PATH
import random
import time
import os
from ..videodownloader import download_video

class XhsSpider(scrapy.Spider):
    name = "xhs"
    allowed_domains = ["www.xiaohongshu.com"]
    start_urls = ["https://www.xiaohongshu.com/explore?channel_id=homefeed_recommend"]  # 初始是推荐页URL
    # start_urls = ['https://www.xiaohongshu.com/search_result?keyword=%25E6%2588%2591%25E7%259A%2584%25E4%25B8%2596%25E7%2595%258C&source=web_explore_feed']
    # 第二个是关键词查询需要改links的获取方式
    def parse(self, response):
            # 解析列表页，获取页面所有的笔记链接
            note_links = response.xpath('//*[@id="exploreFeeds"]/section/div/a[2]/@href').getall()
            # 在parse方法中添加去重逻辑
            seen_links = set()  # 用于记录已处理的链接
            for link in note_links:
                if link and link not in seen_links:  # 检查链接是否有效且未处理
                    seen_links.add(link)  # 记录新链接
                    full_url = response.urljoin(link)  # 使用urljoin拼接完整URL
                    yield scrapy.Request(
                        url= full_url,
                        # url = 'https://www.xiaohongshu.com/explore/685ac81f000000000b02ce00?xsec_token=ABT5xxECfmjuVxzu44eLiN0aPGQ2Wv8RHexcqaMWl9nU0=&xsec_source=pc_feed',
                        callback=self.parse_note_detail
                    )

    def parse_note_detail(self, response):
        # 设置随机延迟
        time.sleep(random.uniform(1, 3))
        
        # 保存response内容到HTML文件
        # filename = f"note_{int(time.time())}.html"  # 使用时间戳作为文件名
        # with open(filename, 'w', encoding='utf-8') as f:
        #    f.write(response.text)  # 将response内容写入文件

        is_video = False
        video_url = response.xpath('//meta[@name="og:video"]/@content').get()
        if video_url:
            is_video = True

        item = RedbookItem()
        if is_video:
            item['type'] = 'video'
            item['title'] = response.xpath('.//div[contains(@class,"title")]/text()').get() 
            item['author'] = response.xpath('//span[@class="username"]/text()').get() 
            item['time'] = response.xpath('//span[@class="date"]/text()').get().split() 
            item['note_link'] = response.urljoin(response.xpath('.//a[contains(@href,"discovery/item")]/@href').get()) 
            item['author_link'] = response.urljoin(response.xpath('.//a[contains(@class,"author-link")]/@href').get()) 
            item['like_count'] = response.xpath('//meta[@name="og:xhs:note_like"]/@content').get()
            item['comment_count'] = response.xpath('//meta[@name="og:xhs:note_comment"]/@content').get()
            item['collect_count'] = response.xpath('//meta[@name="og:xhs:note_collect"]/@content').get()
            item['keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['description'] = response.xpath('//meta[@name="description"]/@content').get()

            item['media_url'] = response.xpath('//meta[@name="og:video"]/@content').get()

            # 下载视频逻辑
            video_url = item['media_url']
            save_path = os.path.join(VIDEO_STORE_PATH, f"{item['title']}.mp4")
            download_video(video_url, save_path)

        else:
            item['type'] = 'image'
            item['title'] = response.xpath('.//div[contains(@class,"title")]/text()').get() 
            item['author'] = response.xpath('//*[@id="noteContainer"]/div[1]/div/div[1]/a[2]/span/text()').get() 
            item['time'] = response.xpath('//div[@class="bottom-container"]/span[@class="date"]/text()').get() 
            item['note_link'] = response.urljoin(response.xpath('.//a[contains(@href,"discovery/item")]/@href').get()) 
            item['author_link'] = response.urljoin(response.xpath('.//a[contains(@class,"author-link")]/@href').get()) 
            item['like_count'] = response.xpath('//meta[@name="og:xhs:note_like"]/@content').get()
            item['comment_count'] = response.xpath('//meta[@name="og:xhs:note_comment"]/@content').get()
            item['collect_count'] = response.xpath('//meta[@name="og:xhs:note_collect"]/@content').get()
            item['keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['description'] = response.xpath('//meta[@name="description"]/@content').get()

            urls = response.xpath('//img[@class="note-slider-img"]/@src').getall()

            item['media_url'] = response.xpath('//meta[@name="og:image"]/@content').get()
            # item['media_url'] = response.xpath('//img[@class="note-slider-img"]/@src').getall() 读取不到,动态加载

        
        yield item
            
        



        
        

