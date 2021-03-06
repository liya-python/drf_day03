from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Book
from .serializers import BookModelSerializer,BookModelDeSerializer,BookModelSerializerV2


class BookAPIView(APIView):

    def get(self,request,*args,**kwargs):
        '''
        查询图书信息的接口
        :param request:
        :return:
        '''
        book_id = kwargs.get('id')
        if book_id:
            # 查询单个图书
            book_obj = Book.objects.get(pk=book_id)
            data = BookModelSerializer(book_obj).data
            return Response({
                'status':200,
                'message':'查询单个图书成功',
                'results':data
            })
        else:
            object_all = Book.objects.all()
            book_list = BookModelSerializer(object_all,many=True).data
            return Response({
                'status': 200,
                'message': '查询图书成功',
                'results': book_list
            })
    def post(self,request,*args,**kwargs):
        data  = request.data
        serializer = BookModelDeSerializer(data=data)

        # 校验是否合法 raise_exception=True 一旦校验失败 立即抛出异常
        serializer.is_valid(raise_exception=True)
        book_obj = serializer.save()
        return Response({
            'status':200,
            'message':'添加单个图书成功',
            'results':BookModelSerializer(book_obj).data
        })

class BookAPIViewV2(APIView):

    def get(self,request,*args,**kwargs):
        '''
        查询图书信息的接口
        :param request:
        :return:
        '''
        book_id = kwargs.get("id")
        if book_id:
            # 查询单个图书
            book_obj = Book.objects.get(pk=book_id,is_delete=False)
            data = BookModelSerializerV2(book_obj).data
            return Response({
                "status": 200,
                "message": "查询单个图书成功",
                "results": data
            })
        else:
            objects_all = Book.objects.filter(is_delete=False)
            book_list = BookModelSerializerV2(objects_all, many=True).data
            return Response({
                "status": 200,
                "message": "查询所有成功",
                'results': book_list
            })
    def post(self,request,*args,**kwargs):
        '''
        新增单个：传递参数的格式 字典
        新增多个：[{},{},{}] 列表中嵌套字典 每一个字典是一个图书对象
        :param request:
        :return:
        '''
        request_data = request.data
        if isinstance(request_data,dict):  # 添加单个对象
            many = False
        elif isinstance(request_data,list): # 代表添加多个对象
            many = True
        else:
            return Response({
                'status':400,
                'message':'数据格式有误'
            })
        book_ser = BookModelSerializerV2(data=request_data,many=many)
        book_ser.is_valid(raise_exception=True)
        save = book_ser.save()
        return Response({
            "status": 200,
            "message": "添加图书成功",
            'results':BookModelSerializerV2(save,many=many).data
        })

    def delete(self,request,*args,**kwargs):
        '''
        删除单个以及删除多个
        单个删除：获取删除的id 根据id删除  通过动态路由传参 v2/delete/1/  {ids:[1']}
        删除多个：有多个id的时候 {ids:[1,2,3]}
        '''
        book_id = kwargs.get('id')
        if book_id:
            # 删除单个 将删除单个转换为删除多个的参数形式
            ids = [book_id]
        else:
            # 删除多个
            ids = request.data.get('ids')
        # 判断传递过来的图书的id是否在数据库中 且还未删除
        response = Book.objects.filter(pk__in=ids,is_delete=False).update(is_delete=True)
        print(response)
        if response:
            return Response({
                'status':status.HTTP_200_OK,
                'message':'删除成功'
            })
        return Response({
            'status':status.HTTP_400_BAD_REQUEST,
            'message':'删除失败或者图书不存在',
        })


    # def put(self,request,*args,**kwargs):
    #     '''
    #     整体修改单个：修改一个对象的全部字段
    #     :return 修改后的对象
    #     '''
    #     # 修改后的参数
    #     request_data = request.data
    #     # 要修改的图书id
    #     book_id = kwargs.get('id')
    #     if book_id:
    #         try:
    #             book_obj = Book.objects.get(pk=book_id,is_delete=False)
    #         except:
    #             return Response({
    #                 'sattus':status.HTTP_400_BAD_REQUEST,
    #                 'message':'图书不存在',
    #             })
    #         # 前端发送的修改的值需要做安全检验
    #         # 更新参数的时候使用序列化器完成数据的检验
    #         # TODO 如果当前要修改某个对象则需要通过instance来指定你要修改的对象
    #         book_ser = BookModelSerializerV2(data=request_data,instance=book_obj)
    #         book_ser.is_valid(raise_exception=True)
    #         save = book_ser.save()
    #         return Response({
    #             "status": 200,
    #             "message": "更新成功",
    #             'results': BookModelSerializerV2(save).data
    #         })
    #
    #
    #
    # def patch(self,request,*args,**kwargs):
    #     '''
    #     局部更新
    #     '''
    #     # 要修改的参数
    #     request_data = request.data
    #     # 要修改的图书id
    #     book_id = kwargs.get('id')
    #     try:
    #         book_obj = Book.objects.get(pk=book_id,is_delete=False)
    #     except:
    #         return Response({
    #             'sattus':status.HTTP_400_BAD_REQUEST,
    #             'message':'图书不存在',
    #         })
    #     # 前端发送的修改数据的值需要做安全校验
    #     # 更新参数的时候使用序列化器完成数据的校验
    #     # TODO 如果当前要局部修改则需要指定 partial = True 即可
    #     book_ser =BookModelSerializerV2(data=request_data,instance=book_obj,partial=True)
    #     book_ser.is_valid(raise_exception=True)
    #     save = book_ser.save()
    #     return Response({
    #         "status": 200,
    #         "message": "更新成功",
    #         "results": BookModelSerializerV2(save).data
    #     })

    # def patch(self,request,*args,**kwargs):
    #     """
    #     群改接口  修改多个对象
    #     单个修改：pk  传递修改的内容    1   {book_name: "百知教育"}     2   {book_name: "Python"}
    #     多个修改：  多个id   多个要修改的值   确定id对应要修改的值是哪个
    #     [{id:1, book_name: "百知教育"},{id:2, price: 23.4}]
    #     """
    #     request_data = request.data
    #     book_id = kwargs.get('id')
    #     # 如果存在且传递的request_data是字典格式 代表单个修改 群改一个
    #     if book_id and isinstance(request_data,dict):
    #         book_ids = [book_id,] # [1]
    #         request_data = [request_data] #[{}]
    #     # 如果id不存在 传递的参数是列表 修改多个
    #     elif not book_id and isinstance(request_data,list):
    #         book_ids = []
    #
    #         # 将要修改的图书的id放入book_ids中
    #         for dic in request_data:
    #             pk = dic.pop('id',None)
    #             if pk:
    #                 book_ids.append(pk)
    #             else:
    #                 return Response({
    #                     'status':status.HTTP_400_BAD_REQUEST,
    #                     'message':'id不存在',
    #                 })
    #     else:
    #         return Response({
    #             'status':status.HTTP_400_BAD_REQUEST,
    #             'message':'参数有误',
    #         })
    #     # print(request_data)
    #     # print(book_ids)
    #
    #     # TODO 需要对传递过来的id  与 request_data 进行筛选  id对应的图书是否存在
    #     # TODO 如果图书对应的id不存在 移除id  并将id对应的要修改的值一并移除  如果id存在则查询对应的图书对象进行修改
    #     book_list = []  # 所有要修改的图书对象
    #     # new_data = []   # 所有要修改的参数
    #     for pk in book_ids:
    #         try:
    #             book_obj = Book.objects.get(pk=pk)
    #             book_list.append(book_obj)
    #         except:
    #             # 如果图书对象不存在 将id与对应的数量移除
    #             index = book_ids.index(pk)
    #             request_data.pop(index)
    #             # print(request_data)
    #             book_ser = BookModelSerializerV2(data=request_data,
    #                                              instance=book_list,
    #                                              partial=True,
    #                                              context={'request':request},
    #                                              many=True)
    #             book_ser.is_valid(raise_exception=True)
    #             book_ser.save()
    #             return Response({
    #                 "status": status.HTTP_200_OK,
    #                 "message": "批量更新成功",
    #             })
    def patch(self, request, *args, **kwargs):
        """
        群改接口  修改多个对象
        单个修改：pk  传递修改的内容    1   {book_name: "百知教育"}     2   {book_name: "Python"}
        多个修改：  多个id   多个要修改的值   确定id对应要修改的值是哪个
        [{id:1, book_name: "百知教育"},{id:2, price: 23.4}]
        """

        request_data = request.data
        book_id = kwargs.get("id")
        # 如果id存在且传递的request_data是字典格式  代表单个修改  群改一个
        if book_id and isinstance(request_data, dict):
            book_ids = [book_id, ]  # [1]
            request_data = [request_data]  # [{}]
        # 如果id不存在  传递的参数是列表  修改多个
        elif not book_id and isinstance(request_data, list):
            book_ids = []

            # 将要修改的图书的id放入book_ids中
            for dic in request_data:
                pk = dic.pop("id", None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": 'id不存在',
                    })

        # 参数格式有误
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": '参数有误',
            })

        # print(request_data)
        # print(book_ids)

        # TODO 需要对传递过来的id  与 request_data 进行筛选  id对应的图书是否存在
        # TODO 如果图书对应的id不存在 移除id  并将id对应的要修改的值一并移除  如果id存在则查询对应的图书对象进行修改
        book_list = []  # 所有要修改的图书对象
        # new_data = []   # 所有要修改的参数
        for pk in book_ids:
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
            except:
                # 如果图书对象不存在 将id与对应的数据移除
                index = book_ids.index(pk)
                request_data.pop(index)
                # print(request_data)

        book_ser = BookModelSerializerV2(data=request_data,
                                         instance=book_list,
                                         partial=True,
                                         context={"request": request},
                                         many=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "批量更新成功",
            # "results": BookModelSerializerV2(save)
        })