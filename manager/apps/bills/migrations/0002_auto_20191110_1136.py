# Generated by Django 2.2.7 on 2019-11-10 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bill',
            options={'ordering': ('source', 'name', 'date'), 'verbose_name': 'Bill', 'verbose_name_plural': 'Bills'},
        ),
        migrations.AlterModelOptions(
            name='recurrentbill',
            options={'ordering': ('active', 'source', 'name'), 'verbose_name': 'Recurrent Bill', 'verbose_name_plural': 'Recurrent Bills'},
        ),
        migrations.RemoveField(
            model_name='tenantvaluebill',
            name='paid',
        ),
        migrations.AlterField(
            model_name='recurrentbill',
            name='periodicity',
            field=models.CharField(choices=[('monthly', 'monthly'), ('yearly', 'yearly')], default='monthly', help_text='Ignore the day. Bills are generated in the first of every a month / year', max_length=100, verbose_name='Periodicity'),
        ),
    ]
