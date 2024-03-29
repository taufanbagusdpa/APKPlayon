# Generated by Django 2.1.2 on 2019-01-02 07:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='additional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.CharField(max_length=50)),
                ('rating', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('publisher', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='posts',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('slug', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('image', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('view', models.IntegerField()),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2019, 1, 2, 7, 59, 55, 681479))),
                ('created_at', models.DateTimeField(default=datetime.datetime(2019, 1, 2, 7, 59, 55, 681506))),
            ],
        ),
        migrations.AddField(
            model_name='details',
            name='id_posts',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='books.posts'),
        ),
        migrations.AddField(
            model_name='additional',
            name='id_posts',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='books.posts'),
        ),
    ]
