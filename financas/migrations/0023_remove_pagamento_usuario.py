# Generated by Django 5.1.2 on 2024-11-21 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financas', '0022_remove_conta_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagamento',
            name='usuario',
        ),
    ]
