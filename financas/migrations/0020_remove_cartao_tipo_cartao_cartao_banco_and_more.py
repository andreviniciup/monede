# Generated by Django 5.1.2 on 2024-11-20 18:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financas', '0019_alter_categoria_icone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartao',
            name='tipo_cartao',
        ),
        migrations.AddField(
            model_name='cartao',
            name='banco',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cartoes', to='financas.banco'),
        ),
        migrations.AddField(
            model_name='cartao',
            name='limite_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='cartao',
            name='data_fechamento',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='cartao',
            name='data_vencimento',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
