# Generated by Django 5.1.2 on 2024-11-23 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_customuser_email_customuser_email_hash_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(default='Anonymous', max_length=100),
        ),
    ]
