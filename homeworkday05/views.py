from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView,RetrieveAPIView,CreateAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from homeworkday05.serializers import TeacherModelSerializer, UserModelSerializer
# Create your views here.
from homeworkday05.models import Teacher, User
from utils.response import APIResponse


class TeacherGenMixView(RetrieveAPIView,CreateAPIView,UpdateAPIView,DestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherModelSerializer
    lookup_field = 'id'
class TeacherGenMixViews(ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherModelSerializer
    lookup_field = 'id'
class TeacherModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'id'
    def patch(self, request, *args, **kwargs):

        request_data = request.data
        teacher_id = kwargs.get("id")

        if teacher_id and isinstance(request_data, dict):
            teacher_ids = [teacher_id, ]
            request_data = [request_data]

        elif not teacher_id and isinstance(request_data, list):
            teacher_ids = []

            for dic in request_data:
                pk = dic.pop("id", None)
                if pk:
                    teacher_ids.append(pk)
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": 'id不存在',
                    })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": '参数有误',
            })
        teacher_list = []

        for pk in teacher_ids:
            try:
                book_obj = Teacher.objects.get(pk=pk)
                teacher_list.append(book_obj)
            except:

                index = teacher_ids.index(pk)
                request_data.pop(index)


        teacher_ser = TeacherModelSerializer(data=request_data,
                                         instance=teacher_list,
                                         partial=True,
                                         context={"request": request},
                                         many=True)
        teacher_ser.is_valid(raise_exception=True)
        teacher_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "批量更新成功",

        })

class UserModelViewSet(ViewSet):
    def user_register(self,request, *args, **kwargs):
        request_data = request.data
        serializer = UserModelSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        teacher_obj = serializer.save()
        return APIResponse(results=UserModelSerializer(teacher_obj).data,data_message='创建用户成功')
class UseViewSet(ViewSet):
    def user_login(self,request, *args, **kwargs):
        request_data = request.data
        username = request_data.get('username')
        password = request_data.get('password')
        if User.objects.filter(username=username,password=password):
            return Response({
                "status": 200,
                "message": "登录成功",
            })
