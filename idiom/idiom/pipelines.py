from itemadapter import ItemAdapter
from dotenv import load_dotenv
import os
import random

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query

from .util import DataTypeEnum

current_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
env_path = os.path.join(current_dir, ".env.prod")  # 爬虫到环境
print(env_path, "hhh")
load_dotenv(dotenv_path=env_path)


class IdiomPipeline:
    databseId: str = os.getenv("DATABASE_ID")
    adminIds: list[str] = os.getenv("USER_ADMINS_ID").split(",")

    def __init__(self) -> None:
        client = Client()
        client.set_endpoint(os.getenv("ENDPOINT_ADRESS"))  # Your API Endpoint
        client.set_project(os.getenv("PROJECT_ID"))  # Your project ID
        client.set_key(os.getenv("API_KEY"))  # Your secret API key

        self.db: Databases = Databases(client)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if item["sort"] == DataTypeEnum.Text.value:
            self._process_text(adapter)
        return item

    # 处理文本
    def _process_text(self, item: ItemAdapter):
        # 判断是否存在内容
        if not item.get("content"):
            return

        # 查询是否存在
        collection_id = "texts"
        queries = [Query.equal("content", item.get("content"))]

        try:
            response = self.db.list_documents(
                self.databseId, collection_id, queries=queries
            )
            documents = response["documents"]
        except Exception as e:
            print(f"查询失败: {e}")
            documents = []

        if documents:
            # textId = documents[0]["$id"]
            # if len(types) != len(documents[0]["types"]) or len(tags) != len(
            #     documents[0]["tags"]
            # ):
            #     self.db.update_document(
            #         self.databseId,
            #         collection_id,
            #         textId,
            #         data={
            #             "userId": random.choice(self.adminIds),
            #             "types": types,
            #             "tags": tags,
            #         },
            #     )
            print(f"已更新: {item.get('content')}")
            return

        types = self._process_type(item.get("types"))
        tags = self._process_tag(item.get("tags"))
        # 创建
        return self.db.create_document(
            self.databseId,
            collection_id,
            document_id="unique()",
            data={
                "title": item.get("title", ""),
                "content": item.get("content"),
                "author": item.get("author", None),
                "isPublic": True,
                "userId": random.choice(self.adminIds),
                "types": types,
                "tags": tags,
                "images": item.get("images", None),
                "english": item.get("english", None),
                "explain": item.get("explain", None),
            },
        )

    # 查询类别ID，如果不存在则创建
    def _process_type(self, types: list[dict] = []) -> list[str]:
        if not types:
            return []

        collection_id = "types"
        type_ids = []

        for type_obj in types:
            name = type_obj.get("name")
            description = type_obj.get("description", "")

            queries = [Query.equal("name", name)]

            try:
                response = self.db.list_documents(
                    self.databseId, collection_id, queries=queries
                )
                documents = response["documents"]
            except Exception as e:
                print(f"查询失败: {e}")
                documents = []

            if documents:
                type_ids.append(documents[0]["$id"])
            else:
                type_id = self.db.create_document(
                    self.databseId,
                    collection_id,
                    document_id="unique()",
                    data={
                        "name": name,
                        "description": description,
                        "userId": random.choice(self.adminIds),
                    },
                )["$id"]
                type_ids.append(type_id)

        return type_ids

    # 查询标签ID，如果不存在则创建
    def _process_tag(self, tags: list[dict] = []) -> list[str]:
        if not tags:
            return []

        collection_id = "tags"
        tag_ids = []

        for tag_obj in tags:
            name = tag_obj.get("name")
            description = tag_obj.get("description", "")

            queries = [Query.equal("name", name)]

            try:
                response = self.db.list_documents(
                    self.databseId, collection_id, queries=queries
                )
                documents = response["documents"]
            except Exception as e:
                print(f"查询失败: {e}")
                documents = []

            if documents:
                tag_ids.append(documents[0]["$id"])
            else:
                tag_id = self.db.create_document(
                    self.databseId,
                    collection_id,
                    document_id="unique()",
                    data={
                        "name": name,
                        "description": description,
                        "userId": random.choice(self.adminIds),
                    },
                )["$id"]
                tag_ids.append(tag_id)

        return tag_ids


if __name__ == "__main__":
    print(os.getenv("ENDPOINT_ADRESS"))
    print(os.getenv("PROJECT_ID"))
