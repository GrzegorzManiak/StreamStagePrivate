# Generated by Django 3.2.16 on 2023-02-08 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48, verbose_name='Category Name')),
                ('description', models.TextField(max_length=256, verbose_name='Brief Description')),
                ('splash_photo', models.ImageField(upload_to='events')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.CharField(max_length=32, primary_key=True, serialize=False, unique=True)),
                ('title', models.TextField(default='New Event', verbose_name='Title')),
                ('description', models.TextField(blank=True, max_length=3096, verbose_name='Description')),
                ('primary_media_idx', models.IntegerField(default=0)),
                ('categories', models.ManyToManyField(to='events.Category')),
            ],
        ),
        migrations.CreateModel(
            name='EventMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(null=True, upload_to='events', verbose_name='Photograph')),
                ('description', models.TextField(blank=True, max_length=300, verbose_name='Photograph Description')),
            ],
            options={
                'verbose_name': 'Event Media',
                'verbose_name_plural': 'Event Media',
            },
        ),
        migrations.CreateModel(
            name='EventShowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=64)),
                ('time', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Event Showing',
                'verbose_name_plural': 'Event Showings',
            },
        ),
        migrations.CreateModel(
            name='EventReview',
            fields=[
                ('review_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('body', models.TextField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('likes', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
            options={
                'verbose_name': 'Event Review',
                'verbose_name_plural': 'Event Reviews',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='media',
            field=models.ManyToManyField(blank=True, to='events.EventMedia'),
        ),
        migrations.AddField(
            model_name='event',
            name='showings',
            field=models.ManyToManyField(to='events.EventShowing'),
        ),
        migrations.AddField(
            model_name='event',
            name='streamer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
