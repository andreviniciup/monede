# Generated by Django 5.1.2 on 2024-11-19 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financas', '0014_transacao_forma_pagamento_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banco',
            name='icone',
        ),
        migrations.AddField(
            model_name='banco',
            name='codigo',
            field=models.CharField(default='000', max_length=10, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banco',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos_bancos/'),
        ),
        migrations.AddField(
            model_name='banco',
            name='nome_completo',
            field=models.CharField(default='Banco Padrão', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='banco',
            name='nome',
            field=models.CharField(max_length=50),
        ),
    ]