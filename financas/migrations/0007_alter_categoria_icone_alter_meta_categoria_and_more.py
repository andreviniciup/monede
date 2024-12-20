# Generated by Django 5.1.2 on 2024-11-12 23:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financas', '0006_alter_categoria_options_categoria_icone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='icone',
            field=models.CharField(default='default_icon', max_length=50),
        ),
        migrations.AlterField(
            model_name='meta',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metas', to='financas.categoria'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transacoes', to='financas.categoria'),
        ),
        migrations.CreateModel(
            name='Limit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=200)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('recorrencia', models.CharField(choices=[('mensal', 'Mensal'), ('diario', 'Diário'), ('semanal', 'Semanal'), ('anual', 'Anual')], max_length=10)),
                ('data_inicio', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='limits', to='financas.categoria')),
            ],
        ),
    ]
