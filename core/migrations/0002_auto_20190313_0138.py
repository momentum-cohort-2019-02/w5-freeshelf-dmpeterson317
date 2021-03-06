# Generated by Django 2.1.7 on 2019-03-13 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['-added_on']},
        ),
        migrations.AlterModelOptions(
            name='bookcategory',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(default=None, unique=True),
            preserve_default=False,
        ),
    ]
