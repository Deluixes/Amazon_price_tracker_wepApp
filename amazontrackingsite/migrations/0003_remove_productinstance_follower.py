# Generated by Django 4.0.6 on 2022-08-21 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amazontrackingsite', '0002_amazonpage_follower_productinstance_follower'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productinstance',
            name='follower',
        ),
    ]