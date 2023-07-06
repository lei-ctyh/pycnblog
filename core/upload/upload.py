import asyncio
import os
import ssl

from core.upload.img_transfer import find_md_img, replace_md_img, upload_img_tasks
from core.upload.post import Post
from core.upload.weblog_client import WeblogClient


def upload_file(file_path):
    # markdown路径
    md_path = file_path
    # 所在文件夹
    dir_name = os.path.dirname(md_path)
    # 博客标题
    title, _ = os.path.splitext(os.path.basename(md_path))  # 文件名作为博客标题
    # 图片上传后url
    net_images = []
    # 图片计数
    image_count = 1
    # 取消全局ssl认证
    ssl._create_default_https_context = ssl._create_unverified_context

    with open(md_path, encoding='utf-8') as f:
        description = f.read()
        print(f'markdown读取成功:{md_path}')
        local_images = find_md_img(description)
        print(f'查寻到以下本地图片: '.join(local_images))

        if local_images:  # 有本地图片，异步上传
            asyncio.run(upload_img_tasks(local_images, dir_name, net_images, image_count))
            image_mapping = dict(zip(local_images, net_images))
            description = replace_md_img(md_path, image_mapping)
        else:
            print('无需上传图片')

        post = Post(description=description, title=title, categories=None, mt_keywords="")
        client = WeblogClient()
        client.upload_post(post)
