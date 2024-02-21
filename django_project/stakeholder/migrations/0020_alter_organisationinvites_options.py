# Generated by Django 4.1.13 on 2024-02-21 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stakeholder", "0019_alter_organisationrepresentative_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="organisationinvites",
            options={
                "permissions": [
                    (
                        "can_invite_people_to_organisation",
                        "Can invite people to organisation",
                    )
                ],
                "verbose_name": "Organisation invite",
                "verbose_name_plural": "Organisation invites",
            },
        ),
    ]