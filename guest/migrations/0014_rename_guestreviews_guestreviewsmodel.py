# Generated by Django 3.2.4 on 2021-09-08 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0013_alter_guestreviews_experience'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GuestReviews',
            new_name='GuestReviewsModel',
        ),
    ]
