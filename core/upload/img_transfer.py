import asyncio
import os
import re
import urllib
from urllib import parse

from core.upload.weblog_client import WeblogClient
from core.util.log_util import log


def find_md_img(md):
    """ markdown中的代码内容不需要参与以下的正则匹配 """
    pattern = r"```.*?```"
    md = re.sub(pattern, "", md, flags=re.DOTALL)

    """查找markdown中的图片，排除网络图片(不用上传)"""
    images = re.findall("\\!\\[.*?\\]\\((.*?)\\)", md)
    images += re.findall('<img src="(.*?)"', md)
    images = [i for i in images if not re.match("((http(s?))|(ftp))://.*", i)]
    log.info(f'共找到{len(images)}张本地图片')
    log.info('\n'.join(images))
    return images


def replace_md_img(path, img_mapping):
    """ 替换markdown中的图片链接 """
    with open(path, 'r', encoding='utf-8') as fr:
        md = fr.read()
        for local, net in img_mapping.items():  # 替换图片链接
            md = md.replace(local, net)
    """ 
      img_format 图片样式格式化  与 gen_network_file 替换本地图片地址先搁置
      if conf["img_format"]:
          md_links = re.findall("!\\[.*?\\]\\(.*?\\)", md)
          md_links += re.findall('<img src=.*/>', md)
          for ml in md_links:
              img_url = re.findall("!\\[.*?\\]\\((.*?)\\)", ml)
              img_url += re.findall('<img src="(.*?)"', ml)
              img_url = img_url[0]
              if conf["img_format"] == "typora":
                  zoom = re.findall(r'style="zoom:(.*)%;"', ml)
                  if zoom:
                      md = md.replace(ml, f'<center><img src="{img_url}"  style="width:{zoom[0]}%;" /></center>')
              else:
                  md = md.replace(ml, conf["img_format"].format(img_url))
      if conf["gen_network_file"]:
          path_net = os.path.join(os.path.dirname(path), '_network'.join(os.path.splitext(os.path.basename(path))))
          with open(path_net, 'w', encoding='utf-8') as fw:
              fw.write(md)
              print(f'图片链接替换完成，生成新markdown:{path_net}')
       """
    return md


def get_image_url(t, net_images, image_count):
    """回调，获取url"""
    url = t.result()['url']
    log.info(f'第{image_count[0]}张图片上传成功,url:{url}')
    net_images.append(url)
    image_count[0] += 1


async def upload_img_tasks(local_images_, dir_name, net_images, image_count):
    tasks = []
    for li in local_images_:
        image_full_path = os.path.join(dir_name, li)
        # C:\\Users\\hjsoft\\Nutstore\\1\\我的坚果云\\obsidian\\学习\\assets/ORECAL19C安装/Pasted%20image%2020231107104952.png
        # os.sep
        image_full_path = image_full_path.replace("\\", "/").replace("/", os.sep)
        image_full_path = urllib.parse.unquote(image_full_path)
        task = asyncio.create_task(WeblogClient().upload_img(image_full_path))
        task.add_done_callback(lambda t: get_image_url(t, net_images, image_count))
        tasks.append(task)
    await asyncio.gather(*tasks)
