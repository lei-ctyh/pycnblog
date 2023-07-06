import xmlrpc.client

# 创建 XML-RPC 服务器代理
server = xmlrpc.client.ServerProxy("https://rpc.cnblogs.com/metaweblog/aaalei")

# 获取博客文章的分类列表

recent_posts = server.metaWeblog.getRecentPosts("aaalei", "2468341590@qq.com",
                                                "95529D103516E0289554BD76D87CBABC72811A92F37AEA3ABE3B8266D3A1B5F9", 1)
# 打印分类名称
for recent_post in recent_posts:
    print(recent_post)
