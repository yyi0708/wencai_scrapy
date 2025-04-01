import scrapy
import re

from ..items import IdiomItem
from ..util import DataTypeEnum


class JuzihuiSpider(scrapy.Spider):
    name = "juzihui"
    allowed_domains = ["www.wenzizhan.com"]
    urls = [
        {
            "url": "https://www.wenzizhan.com/juzihui/",
            "sort": DataTypeEnum.Text.value,
        },
        {
            "url": "https://www.wenzizhan.com/juzihui/writers/",
            "sort": DataTypeEnum.Type.value,
        },
    ]

    def start_requests(self):
        for url_obj in self.urls:
            if url_obj["sort"] == DataTypeEnum.Text.value:
                pass
                # yield scrapy.Request(url=url_obj["url"], callback=self.parse)
                # 单条测试
                # yield scrapy.Request(
                #     url="https://www.wenzizhan.com/juzihui/jingdian?page=31",
                #     meta={
                #         "types": [
                #             {
                #                 "name": "名人名句",
                #                 "description": "包含名人名言和经典句子",
                #             }
                #         ],
                #         "tags": [
                #             {
                #                 "name": "名人名句",
                #                 "description": "包含名人名言和经典句子",
                #             }
                #         ],
                #     },
                #     callback=self._parse_idiom_list,
                # )
            elif url_obj["sort"] == DataTypeEnum.Type.value:
                # 名人名言
                # pass
                # yield scrapy.Request(url=url_obj["url"], callback=self.parse_type)
                # 单条测试
                yield scrapy.Request(
                    url="https://www.wenzizhan.com/juzihui/writer/%e7%ba%b3%e5%85%b0%e5%ae%b9%e8%8b%a5/",
                    meta={
                        "types": [
                            {
                                "name": "名人名句",
                                "description": "包含名人名言和经典句子",
                            }
                        ],
                        "tags": [
                            {
                                "name": "名人名句",
                                "description": "包含名人名言和经典句子",
                            }
                        ],
                    },
                    callback=self._parse_page,
                )

    # 类别-解析分页（名人名言）
    def parse_type(self, response):
        try:
            page_end_str = response.css(
                "body .jzrMain .pages a:nth-last-of-type(1)"
            ).attrib["href"]

            types = []
            tags = []
            types.append({"name": "名人名句", "description": "包含名人名言和经典句子"})
            tags.append({"name": "名人名句", "description": "包含名人名言和经典句子"})

            if page_end_str:
                page_end = int(page_end_str.split("page=")[1])
                for i in range(1, page_end + 1):
                    url = response.url + f"?page={i}"
                    yield scrapy.Request(
                        url,
                        meta={"types": types, "tags": tags},
                        callback=self._parse_type_list,
                    )

        except Exception as e:
            print(e, f"err: in type 1 {response.url}")

    # 类别-解析列表（名人名言
    def _parse_type_list(self, response):
        try:
            for selector in response.css("body .juziMain .pContent .itemU"):
                # icon = selector.css("a img").attrib["src"].get(default="")
                url = selector.css(".divName a").attrib["href"]
                author = selector.css(".divName a::text").get(default="").strip()
                description = selector.css(".divDescript *::text").getall()

                types = response.meta["types"]
                tags = response.meta["tags"] + (
                    [{"name": author, "description": description}] if author else []
                )

                yield scrapy.Request(
                    url,
                    meta={"types": types, "tags": tags},
                    callback=self._parse_page,
                )
        except Exception as e:
            print(e, f"err: in type 2 {response.url}")

    # 1. 文本-解析分类
    def parse(self, response):
        for selector in response.css("body div.theMain .ltItem  .ajuzitype"):
            url = selector.attrib["href"]
            type_name = selector.css(".spanMain .s1::text").get(default="").strip()
            type_description = (
                selector.css(".spanMain .s2::text").get(default="").strip()
            )

            # 定义文本所属类别、标签
            types = []
            tags = []
            types.append({"name": type_name, "description": type_description})

            yield scrapy.Request(
                url,
                meta={"types": types, "tags": tags},
                callback=self._parse_page,
            )

    # 2. 文本-解析分页
    def _parse_page(self, response):
        try:
            page_end_str = response.css("body .pages a:nth-last-child(1)").attrib[
                "href"
            ]

            if page_end_str:
                page_end = int(page_end_str.split("page=")[1])
                for i in range(1, page_end + 1):
                    url = response.url + f"?page={i}"
                    yield scrapy.Request(
                        url,
                        meta=response.meta,
                        callback=self._parse_idiom_list,
                    )
            print("page_end_str", page_end_str)

        except Exception as e:
            print(e, "err: in step 2")
            print(response.url)

    # 3. 文本-解析成语列表
    def _parse_idiom_list(self, response):
        try:
            types = response.meta["types"]
            tags = response.meta["tags"]
            print("crawl url", response.url)

            for selector in response.css("body .pContent .lcItem"):
                idiom = IdiomItem()
                tags_after = []

                contents = [
                    re.sub(r"\s+", " ", text.strip())
                    for text in selector.css(".d1 *::text").extract()
                    if text.strip()
                ]
                authors = selector.css(".d2 a::text").getall()
                author_str = ""
                for author in authors:
                    author = re.sub(r"\s+", " ", author.strip())
                    if author:
                        author_str = (
                            (author + " " + author_str) if author_str else author
                        )
                        tags_after.append({"name": author, "description": ""})

                idiom["sort"] = DataTypeEnum.Text.value
                idiom["content"] = "\n".join(contents)
                idiom["author"] = " ".join(author_str)
                idiom["types"] = types
                idiom["tags"] = tags_after
                idiom["title"] = None
                print("idiom", idiom)

                yield idiom
        except Exception as e:
            print(e, "err: in step 3")
            print(response.url)
