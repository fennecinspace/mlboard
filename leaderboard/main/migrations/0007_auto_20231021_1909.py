# Generated by Django 3.2 on 2023-10-21 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20231018_1557'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ressource',
            new_name='Resource',
        ),
        migrations.AlterField(
            model_name='submission',
            name='file',
            field=models.FileField(upload_to='submissions/'),
        ),
    ]