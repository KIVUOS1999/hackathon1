# Generated by Django 3.0.3 on 2021-02-02 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210126_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='imageSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_image', models.ImageField(upload_to='')),
            ],
        ),
    ]
