from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from api.models import Book
from app.serializers import BookModelSerializer
from utils.response import APIResponse
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, \
    UpdateModelMixin
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView


# GenericAPIView继承了APIView，向上兼容
class BookGenericAPIView(ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin,
                         GenericAPIView):
    # 获取当前视图操作的模型的数据  以及序列化器类
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer

    # 指定查询单个对象的参数
    lookup_field = "id"

    # 查询接口
    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    # 新增图书
    def post(self, request, *args, **kwargs):
        create = self.create(request, *args, **kwargs)
        return APIResponse(results=create.data, data_message="新增方便")

    # 单整体改
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return APIResponse(results=response.data)

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(results=response.data)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    """
    def get(self, request, *args, **kwargs):
        # 获取所有的图书对象
        # objects_all = Book.objects.filter(is_delete=False)
        objects_all = self.get_queryset()
        # 获取当前视图要使用的序列化器
        # serializer = BookModelSerializer(objects_all, many=True).data
        book_ser = self.get_serializer(objects_all, many=True).data

        return APIResponse(results=book_ser)

    def get(self, request, *args, **kwargs):
        # book_id = kwargs.get('pk')
        # print(book_id)
        # book_obj = Book.objects.get(pk=book_id)
        # data = BookModelSerializer(book_obj).data
        book_obj = self.get_object()
        print(book_obj)
        serializer = self.get_serializer(book_obj).data

        return APIResponse(results=serializer)
    """


class BookGenericMixinView(ListAPIView, RetrieveAPIView, CreateAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"


class BookModelViewSet(ModelViewSet):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"

    """定义登录操作"""

    def user_login(self, request, *args, **kwargs):
        # 可以再此方法中完成用户登录
        request_data = request.data
        print(request_data)
        return self.list(request, *args, **kwargs)

    def get_user_count(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class BookViewSetAPIView(ViewSet):

    def read_execle(self, request, *args, **kwargs):
        pass

