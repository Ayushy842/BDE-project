# Generated by Django 4.2.3 on 2023-07-13 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_round2_screenshot_shared'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bde_user',
            name='username',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='round1',
            name='screenshot_shared',
            field=models.ImageField(blank=True, null=True, upload_to='screenshots/'),
        ),
        migrations.AlterField(
            model_name='round2',
            name='screenshot_shared',
            field=models.ImageField(blank=True, null=True, upload_to='screenshots/'),
        ),
        migrations.AlterField(
            model_name='round3',
            name='screenshot_shared',
            field=models.ImageField(blank=True, null=True, upload_to='screenshots/'),
        ),
    ]
