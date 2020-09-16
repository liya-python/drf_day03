from rest_framework.serializers import ModelSerializer
from homeworkday05.models import Teacher, User
from rest_framework import serializers, exceptions


class TeacherListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        for index,obj in enumerate(instance):
            self.child.update(obj,validated_data[index])
        return instance
class TeacherModelSerializer(ModelSerializer):
    class Meta:
        list_serializer_class = TeacherListSerializer
        model = Teacher
        fields = ('teacher_name','age','gender','phone','email','address','course')

class UserListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        for index,obj in enumerate(instance):
            self.child.update(obj,validated_data[index])
        return instance

class UserModelSerializer(ModelSerializer):
    class Meta:
        list_serializer_class = UserListSerializer
        model = User
        fields = ('username','password')

    def validate(self,attrs):
        name = attrs.get('username')
        user = User.objects.filter(username=name)
        if user:
            raise exceptions.ValidationError('用户名已存在')