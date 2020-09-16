from rest_framework.serializers import ModelSerializer
from rest_framework import serializers, exceptions

class BookModelSerializer(ModelSerializer):
    """
    序列化器与反序列化器整合
    """

    class Meta:
        # 为修改多个图书提供ListSerializer
        list_serializer_class = BookListSerializer

        model = Book
        # 指定的字段  填序列化与反序列所需字段并集
        fields = ("book_name", "price", "pic", "publish", "authors")

        # 添加DRF的校验规则  可以通过此参数指定哪些字段只参加序列化  哪些字段只参加反序列化
        extra_kwargs = {
            "book_name": {
                "max_length": 18,  # 设置当前字段的最大长度
                "min_length": 2,
            },
            # 只参与反序列化
            "publish": {
                "write_only": True,  # 指定此字段只参与反序列化
            },
            "authors": {
                "write_only": True,
            },
            # 只参与序列化
            "pic": {
                "read_only": True
            }
        }


