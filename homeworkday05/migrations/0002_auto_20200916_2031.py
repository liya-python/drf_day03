# Generated by Django 2.0.6 on 2020-09-16 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeworkday05', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'bz_user',
            },
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': '课程', 'verbose_name_plural': '课程'},
        ),
    ]