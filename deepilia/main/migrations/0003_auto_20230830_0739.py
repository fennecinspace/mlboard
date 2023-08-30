# Generated by Django 3.2 on 2023-08-30 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_member_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='thesis',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.thesis'),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='advisors',
            field=models.ManyToManyField(blank=True, related_name='supervisions', to='main.Member'),
        ),
    ]
