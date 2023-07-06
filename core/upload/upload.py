import asyncio
import html
import os
import ssl
import sys
import xmlrpc


from core.upload.config_loader import conf
from core.upload.img_transfer import upload_img, find_md_img, replace_md_img
from core.upload.server_proxy import server


def get_image_url(t, net_images, image_count):
    """回调，获取url"""
    url = t.result()['url']
    print(f'第{image_count}张图片上传成功,url:{url}')
    net_images.append(url)
    image_count += 1


def cancel_ssh_authentication():  # 取消全局ssl认证

    ssl._create_default_https_context = ssl._create_unverified_context


async def upload_tasks(local_images_, dir_name, net_images, image_count):
    tasks = []
    for li in local_images_:
        image_full_path = os.path.join(dir_name, li)
        task = asyncio.create_task(upload_img(image_full_path))
        task.add_done_callback(lambda t: get_image_url(t, net_images, image_count))
        tasks.append(task)
    await asyncio.gather(*tasks)


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

    cancel_ssh_authentication()
    with open(md_path, encoding='utf-8') as f:
        md = f.read()
        print(f'markdown读取成功:{md_path}')
        local_images = find_md_img(md)
        print(f'查寻到以下本地图片: '.join(local_images))

        if local_images:  # 有本地图片，异步上传
            asyncio.run(upload_tasks(local_images, dir_name, net_images, image_count))
            image_mapping = dict(zip(local_images, net_images))
            md = replace_md_img(md_path, image_mapping)
        else:
            print('无需上传图片')

        post = dict(
            description=md,
            title=title,
            categories=['[Markdown]'] + conf["categories"],
            mt_keywords="你好",
            mt_excerpt="我是一段摘要"
        )



        recent_posts = server.metaWeblog.getRecentPosts(conf["blog_id"], conf["username"], conf["password"], 99)
        # 获取所有标题，需要处理HTML转义字符
        recent_posts_titles = [html.unescape(recent_post['title']) for recent_post in recent_posts]
        if title not in recent_posts_titles:
            server.metaWeblog.newPost(conf["blog_id"], conf["username"], conf["password"], post, conf["publish"])
            print(f"markdown上传成功, 博客标题为'{title}', 状态为'{'已发布' if conf['publish'] else '未发布'}', "
                  f"分类为:{conf['categories']} 请到博客园后台查看")
        else:
            for recent_post in recent_posts:
                if title == html.unescape(recent_post['title']):
                    update_post = recent_post
                    update_post['description'] = md
                    # 博客更新时保留摘要、标签
                    posted_article = server.metaWeblog.getPost(update_post['postid'], conf["username"],
                                                               conf["password"])
                    try:
                        update_post["mt_keywords"] = posted_article["mt_keywords"]
                        update_post["mt_excerpt"] = posted_article["mt_excerpt"]
                    except KeyError:
                        pass
                    try:
                        server.metaWeblog.editPost(update_post['postid'], conf["username"], conf["password"],
                                                   update_post,
                                                   conf["publish"])
                    except xmlrpc.client.Fault as fault:
                        if 'published post can not be saved as draft' in str(fault):
                            server.metaWeblog.editPost(update_post['postid'], conf["username"], conf["password"],
                                                       update_post, True)
                        else:
                            raise fault
                    print(f"博客'{title}'更新成功")
