# Generated by Django 3.2.5 on 2021-10-09 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(null=True, verbose_name='Date of birth'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default=None, max_length=254, unique=True),
            preserve_default=False,
        ),
    ]
