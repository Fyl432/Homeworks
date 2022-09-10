# Generated by Django 4.0.4 on 2022-05-03 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0002_alter_author_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcategory',
            options={'verbose_name': 'Связь', 'verbose_name_plural': 'Связи'},
        ),
        migrations.AlterField(
            model_name='postcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='News.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='postcategory',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='News.post', verbose_name='Пост'),
        ),
    ]
