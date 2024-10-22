# Generated by Django 4.0.4 on 2022-04-22 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_company_name'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='client',
            name='is_reachable',
        ),
        migrations.AddConstraint(
            model_name='client',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('email__isnull', True), _negated=True), models.Q(('phone__isnull', True), _negated=True), models.Q(('mobile__isnull', True), _negated=True), _connector='OR'), name='is_reachable'),
        ),
    ]
