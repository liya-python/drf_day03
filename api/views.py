from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Employee
from  .serializers import EmployeeSerializer,EmployeeDeSerializer



class EmployeeAPIView(APIView):
    def get(self,request,*args,**kwargs):
        '''
        查询接口
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        user_id = kwargs.get('id')
        if user_id:
            #查询单个
            emp_obj = Employee.objects.get(pk=user_id)
            if user_id:
                # 使用定义好的序列化器完成数据的序列化
                # .data 将序列化后的数据打包成字典
                emp_ser = EmployeeSerializer(emp_obj).data
                print(emp_ser,type(emp_ser))
                return Response({
                    'status':200,
                    'message':'查询单个成功',
                    'results':emp_ser
                })
        else:
            # 查询所有
            object_all = Employee.objects.all()
            # 使用序列化器完成数据的序列化
            # 当序列化器序列多个对象时，可以指定参数
            all_data = EmployeeSerializer(object_all,many=True).data
            return Response({
                'status': 200,
                'message': '查询所有成功',
                'results': all_data
            })
    def post(self, request, *args, **kwargs):
        """
        接受数据保存入库
        :param request:
        :return:
        """
        user_data = request.data
        # print(user_data)

        # TODO 前端发送的数据需要入库时  必须对前端发送来的数据做校验
        if not isinstance(user_data, dict) or user_data == {}:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "请求数据格式有误"
            })

        # 使用序列化器对前端提交的数据进行反序列化
        # 需要反序列化数据在传递时需要指定关键字  data
        serializer = EmployeeDeSerializer(data=user_data)
        # print(serializer)

        # 对序列化的数据进行校验  通过is_valid() 方法对传递到序列化器类的数据进行校验
        # print(serializer.is_valid())
        if serializer.is_valid():
            # 数据校验通过后才进行保存  调用save()保存数据  需要在序列化器中重写create()方法完成数据的入库
            emp_obj = serializer.save()
            # print(emp_obj, "this is obj", type(emp_obj))

            return Response({
                "status": status.HTTP_200_OK,
                "message": "用户保存成功",
                "results": EmployeeSerializer(emp_obj).data
            })

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": serializer.errors
        })
