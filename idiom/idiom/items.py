# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 类型
class TypeItem(scrapy.Item):
    sort = scrapy.Field()  # 分类
    name = scrapy.Field()
    description = scrapy.Field()


# 标签
class TagItem(scrapy.Item):
    sort = scrapy.Field()  # 分类
    name = scrapy.Field()
    description = scrapy.Field()


# 文字
class IdiomItem(scrapy.Item):
    sort = scrapy.Field()  # 分类
    types = scrapy.Field()  # 类型 list[{"name": "类型", "description": "描述"}]
    tags = scrapy.Field()  # 标签 list[{"name": "类型", "description": "描述"}]
    title = scrapy.Field()  # 标题
    content = scrapy.Field()  # 内容
    author = scrapy.Field()  # 作者
    images = scrapy.Field()  # 图片
    english = scrapy.Field()  # 英文
    explain = scrapy.Field()  # 解释
