from django.db import models


class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    class Meta:
        # 在原数据中可以通过abstract来表明当前为抽象表 不会在数据库中为当前表生产对应的表结构
        # 其他模型继承这个抽象表后，可以继承表中拥有的字段
        abstract = True

class Book(BaseModel):
    book_name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    pic = models.ImageField(upload_to='img',default="img/1.jpg")
    publish = models.ForeignKey(to='Press',on_delete=models.CASCADE,# 级联删除
                                db_constraint=False,# 删除后对应的字段可以为空
                                related_name='books',#反向查询的名称
                                )
    author = models.ManyToManyField(to='Author',db_constraint=False,related_name='books')

    # def aaa(self):
    #     return 'aaa'

    # 自定义序列化器所需的字段 使用方法作为属性
    @property # 类属性
    def press_name(self):
        # print(type(self.publish))
        # print(self.publish.press_name,type(self.publish.press_name))
        return self.publish.press_name
    @property
    def press_address(self):
        return self.publish.address
    @property
    def author_list(self):
        return self.author.values('author_name','age','detail__phone')


    class Meta:
        db_table = 'bz_book'
        verbose_name = '图书表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.book_name


class Press(BaseModel):
    press_name = models.CharField(max_length=128)
    pic = models.ImageField(upload_to='img',default="img/1.jpg")
    address = models.CharField(max_length=256)

    @property
    def img(self):
        return "%s%s" % ('http://127.0.0.1:8000/',self.pic)

    class Meta:
        db_table= 'bz_press'
        verbose_name = '出版社'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.press_name

class Author(BaseModel):
    author_name = models.CharField(max_length=128)
    age = models.IntegerField()

    class Meta:
        db_table= 'bz_author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author_name

class AuthorDetail(BaseModel):
    phone = models.CharField(max_length=11)
    author = models.OneToOneField(to="Author",on_delete=models.CASCADE,related_name='detail')

    class Meta:
        db_table= 'bz_author_detail'
        verbose_name = '作者详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s的详情" % self.author.author_name



class Employee(models.Model):
    gender_choices = (
        (0,'male'),
        (1,'female'),
        (2,'other'),
    )
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=64)
    gender = models.SmallIntegerField(choices=gender_choices,default=0)
    phone = models.CharField(max_length=11,null=True,blank=True)
    pic = models.ImageField(upload_to='pic',default='pic/1.jig')
    class Meta:
        db_table = 'bz_employee'
        verbose_name = '员工'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username