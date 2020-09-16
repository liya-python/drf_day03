from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework import exceptions

from api.models import Book, Press


class PressModelSerializer(ModelSerializer):
    '''
    出版社的序列化器
    '''
    class Meta:
        model = Press
        fields = ('press_name','address','img')

class BookModelSerializer(ModelSerializer):
    '''
    图书的序列化
    '''
    # 提供自定义字段 不推荐使用
    # aaa = serializers.SerializerMethodField()
    # def get_aaa(self,obj):
    #     return 'aaa'

    # TODO 自定义序列化器连表查询 查询图书时将对应的出版社的信息查询出来
    # 可以在图书的序列化器中嵌套一个序列化器完成多表查询
    # 必须与模型中的外键名保持一致  在连表查询较多字段是使用
    publish = PressModelSerializer()
    class Meta:
        # 指定当前序列化器要序列化哪个模型
        model = Book
        # 指定序列化模型的字段
        # fields = ('book_name','price','pic','press_name','press_address','author_list')
        fields = ('book_name','price','pic','publish')

        # 可以直接查询表的所有字段
        # fields = '__all__'

        #  指定不展示哪些字段
        # exclude = ('is_delete','status','id')

        # 指定查询的深度
        # depth = 1

class BookModelDeSerializer(ModelSerializer):
    '''
    图书的反序列化
    '''
    class Meta:
        model = Book
        fields = ('book_name','price','publish','author')
        # 为反序列化器添加验证规则
        extra_kwargs = {
            'book_name':{
                'max_length':18, # 设置当前字段的最大长度
                'min_length':2,
                'error_messages':{
                    'max_length':'长度过长',
                    'min_length':'长度过短',
                }
            },
            'price':{
                'required':True, # 设置必填项
                'decimal_places':2,
            }
        }
    # 全局钩子同样适用于 ModelSerializer
    def validate(self, attrs):
        name = attrs.get("book_name")
        book = Book.objects.filter(book_name=name)
        if len(book) > 0:
            raise exceptions.ValidationError('图书名已存在')

        return attrs
    # 局部钩子的使用 验证某个字段
    def validate_price(self,obj):
        # 价格不能超过1000
        if obj > 1000:
            raise exceptions.ValidationError("价格最多不能超过10000")
        return obj

class BookModelSerializerV2(ModelSerializer):
    """
    序列化器与反序列化器整合
    """

    class Meta:
        model = Book
        # 指定的字段  填序列化与反序列所需字段并集
        fields = ("book_name", "price", "pic", "publish", "author")

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
        # 全局钩子同样适用于 ModelSerializer

    def validate(self, attrs):
        name = attrs.get("book_name")
        book = Book.objects.filter(book_name=name)
        if len(book) > 0:
            raise exceptions.ValidationError('图书名已存在')

        return attrs

        # 局部钩子的使用  验证每个字段

    def validate_price(self, obj):
        # 价格不能超过1000
        if obj > 1000:
            raise exceptions.ValidationError("价格最多不能超过10000")
        return obj

    # 重写update方法完成更新
    # def update(self, instance, validated_data):
    #     print(instance, "11111")
    #     print(validated_data)
    #     book_name = validated_data.get("book_name")
    #     instance.book_name = book_name
    #     instance.save()
    #     return instance

