# Generated by Django 3.2 on 2023-10-18 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=512, null=True)),
                ('description', models.TextField(blank=True, max_length=3000)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('processor', models.URLField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Ressource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('file', models.FileField(blank=True, null=True, upload_to='files/')),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('score', models.FloatField(blank=True)),
                ('status', models.CharField(choices=[('ERROR', 'ERROR'), ('PROCESSING', 'PROCESSING'), ('IN-QUEUE', 'IN-QUEUE'), ('DONE', 'DONE')], default='IN-QUEUE', max_length=200)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.challenge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='files',
            field=models.ManyToManyField(blank=True, to='main.Ressource'),
        ),
    ]
