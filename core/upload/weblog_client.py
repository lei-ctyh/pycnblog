import html
import os
import tempfile
import xmlrpc.client

import yaml

from core.upload.mime import mime_mapping
from core.upload.post import Post
from core.util.log_util import log


class WeblogClient:
    blog_url = ""
    blog_id = ""
    username = ""
    password = ""
    publish = ""
    categories = None

    client = None

    def __init__(self):
        # 初始化yaml数据
        config_path = os.path.join(os.path.join(tempfile.gettempdir(), 'pycnblog'), "config.yaml")
        with open(config_path, "r", encoding="utf-8") as f:
            conf = yaml.load(f.read(), Loader=yaml.FullLoader)

        # 初始化上传服务承参数
        self.blog_url = conf["blog_url"].strip()
        self.blog_id = conf["blog_id"].strip()
        self.username = conf["username"].strip()
        self.password = conf["password"].strip()
        self.publish = conf["publish"]

        try:
            server = xmlrpc.client.ServerProxy(self.blog_url)
            self.client = server.metaWeblog
        except Exception as e:
            e = str(e)
            if 'unsupported XML-RPC protocol' in e:
                print('请检查blog_url,应该是这个URL地址没设置对')

    def upload_post(self, post):
        log.info("文章上传开始")
        # 所有的文章
        recent_posts = self.client.getRecentPosts(self.blog_id, self.username, self.password, 99)
        is_edit_post = False
        for recent_post in recent_posts:
            if post.title == html.unescape(recent_post['title']):
                update_post = Post(post_dict=recent_post)
                update_post.description = post.description
                log.info("更新一篇文章")

                try:
                    self.client.editPost(update_post.postid, self.username, self.password, update_post, self.publish)
                except xmlrpc.client.Fault as fault:
                    if 'published post can not be saved as draft' in str(fault):
                        # 已发布的帖子无法存为草稿
                        self.client.editPost(update_post.postid, self.username, self.password, update_post, True)
                    else:
                        raise fault
                is_edit_post = True

        if not is_edit_post:
            log.info("新增一篇文章")
            self.client.newPost(self.blog_url, self.username, self.password, post.to_dict(), self.publish)
        log.info("文章上传成功")

    async def upload_img(self, img_path):
        """上传图片"""
        img_name = os.path.basename(img_path)
        _, file_type = os.path.splitext(img_name)
        with open(img_path, 'rb') as f:
            file = {
                "bits": f.read(),
                "name": img_name,
                "type": mime_mapping[file_type]
            }
            img_url = self.client.newMediaObject(self.blog_id, self.username, self.password, file)
            return img_url
