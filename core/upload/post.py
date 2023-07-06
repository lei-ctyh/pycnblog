class Post:
    """ 文章创建时间 """
    dateCreated = None
    """ 文章主要内容 """
    description = ""
    """ 文章标题 """
    title = ""
    """ 文章分类,是个list,可以为空 """
    categories = []
    """ 链接 """
    link = ""
    """ 文章永久链接, 现在默认等同于link """
    permalink = ""
    """ 文章id """
    postid = ""
    """ 更多 """
    mt_text_more = ""
    """ 文章摘要 """
    mt_excerpt = ""
    """ 文章标签 不同标签直接用英文逗号分割"""
    mt_keywords = ""

    def __init__(self, title="", description="", categories=None, mt_keywords="", post_dict=None):
        if categories is None:
            categories = []
        if post_dict is not None:
            for key, value in post_dict.items():
                setattr(self, key, value)
        self.title = title
        self.description = description
        self.categories = categories
        self.mt_keywords = mt_keywords

    def to_dict(self):
        return vars(self)
