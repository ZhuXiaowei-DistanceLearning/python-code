import requests
from lxml import etree
import os
import time
import uuid


class QuibaiSpdier:

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}
        self.url = "https://www.qiushibaike.com/img/0.html"
        
    def get_url_list(self):
        return [self.url_temp.format(i) for i in range(14)]
        
    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        response.encoding = "utf-8"
        return response.text
    
    def tow_parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content
        
    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        content_list = []
        list = html.xpath("//div[contains(@class,'pic-wrapper')]")
        for li in list:
            item = {}
            imgurl = li.xpath("./a/div/@style")[0]
            item['imgurl'] = "https://" + imgurl.split("//")[1].split(")")[0]
            item['number'] = li.xpath("./a/div/span/text()")
            item["title"] = li.xpath("./a/div/following-sibling::span/text()")
            content_list.append(item)
        return content_list
    
    def get_img_content(self, url, filename):
        img_str = self.tow_parse_url(url)
        with open(filename,'wb') as f:
            f.write(img_str)
        print("保存成功")
        
    def run(self):  # 实现主要逻辑
        next_url = self.url;
        # 1.url_list
       # url_list = self.get_url_list()
        # 2.遍历，发送请求，获取响应
        html_str = self.parse_url(next_url);
        # 3.存取图片数据到列表
        content_list = self.get_content_list(html_str);
        # 4.提取数据
        print("开始循环")
        base_imgdir = "C:\\Users\\zxw\\Desktop\\qiubai"
        os.chdir(base_imgdir)
        current_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        category=current_day+str(uuid.uuid4())
        os.mkdir(category)
        os.chdir(category)
        for i in range(len(content_list)):
            filename = content_list[i]['imgurl'].split('/')[-3] + ".png"
            img_url = content_list[i]['imgurl']
            self.get_img_content(img_url, filename)
        # 4.保存
        print("所有图片保存成功，程序结束")
        
if __name__ == '__main__':
    qs = QuibaiSpdier();
    qs.run()
    
