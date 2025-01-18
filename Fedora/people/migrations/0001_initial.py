# Generated by Django 5.1.4 on 2025-01-11 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.CharField(max_length=50)),
                ('last', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'People',
            },
        ),
    ]
