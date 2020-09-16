from django.db import models

# Create your models here.
class Teacher(models.Model):
    gender_choices = (
        (0, 'male'),
        (1, 'female'),
        (2, 'other'),
    )
    teacher_name = models.CharField(max_length=80)
    age = models.IntegerField()
    gender = models.IntegerField(choices=gender_choices,default=0)
    phone = models.CharField(max_length=11,null=True,blank=True)
    email = models.CharField(max_length=40)
    address = models.CharField(max_length=256)
    course = models.ManyToManyField(to='Course',db_constraint=False,related_name='teachers')
    class Meta:
        db_table = 'bz_teacher'
        verbose_name = '教师'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.teacher_name

class Course(models.Model):
    course_name = models.CharField(max_length=40)
    time = models.CharField(max_length=30)
    class Meta:
        db_table = 'bz_course'
        verbose_name = '课程'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.course_name


class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=40)
    class Meta:
        db_table = 'bz_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username


