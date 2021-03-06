# Generated by Django 2.2.4 on 2019-08-29 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0003_auto_20190829_2243'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pattern',
            options={'default_related_name': 'patterns', 'ordering': ('day',)},
        ),
        migrations.AlterField(
            model_name='pattern',
            name='day',
            field=models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (0, 'Sunday')]),
        ),
        migrations.AlterField(
            model_name='pattern',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patterns', to='schedules.ScheduleRule'),
        ),
    ]
