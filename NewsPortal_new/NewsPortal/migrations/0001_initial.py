# Generated by Django 4.1.7 on 2023-03-02 17:14

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
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate_user', models.IntegerField(default=0)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Sport', 'Спорт'), ('Politics', 'Политика'), ('Lern', 'Образование'), ('Play', 'Развлечения'), ('Rest', 'Досуг')], default='Rest', max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=50, null=True)),
                ('p_post', models.TextField()),
                ('p_create_date', models.DateTimeField(auto_now_add=True)),
                ('p_update_date', models.DateTimeField(auto_now=True)),
                ('p_rate', models.IntegerField(default=0)),
                ('p_type', models.CharField(choices=[('Post', 'Статья'), ('News', 'Новость')], default='Post', max_length=20)),
                ('p_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal.author')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pc_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal.category')),
                ('pc_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='p_category',
            field=models.ManyToManyField(through='NewsPortal.PostCategory', to='NewsPortal.category'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_post', models.TextField()),
                ('c_create_date', models.DateTimeField(auto_now_add=True)),
                ('c_rate', models.IntegerField(default=0)),
                ('com_auth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('com_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal.post')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='cat_post',
            field=models.ManyToManyField(through='NewsPortal.PostCategory', to='NewsPortal.post'),
        ),
    ]
