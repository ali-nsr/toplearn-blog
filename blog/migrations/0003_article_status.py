# Generated by Django 4.2.2 on 2023-07-07 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_tag_article_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('d', 'draft'), ('p', 'published')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
