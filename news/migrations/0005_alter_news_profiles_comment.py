# Generated by Django 4.2.7 on 2023-12-04 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_profiles_news_profiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='profiles',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='news.profiles', verbose_name='Профиль'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('content', models.TextField(blank=True, verbose_name='Контент')),
                ('news', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='news.news', verbose_name='Новость')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='news.profiles', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]