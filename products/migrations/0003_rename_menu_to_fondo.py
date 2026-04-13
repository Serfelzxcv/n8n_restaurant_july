from django.db import migrations, models


def forwards_rename_menu_to_fondo(apps, schema_editor):
    Plato = apps.get_model('products', 'Plato')
    Plato.objects.filter(categoria='menu').update(categoria='fondo')


def backwards_rename_fondo_to_menu(apps, schema_editor):
    Plato = apps.get_model('products', 'Plato')
    Plato.objects.filter(categoria='fondo').update(categoria='menu')


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_plato_delete_product'),
    ]

    operations = [
        migrations.RunPython(forwards_rename_menu_to_fondo, backwards_rename_fondo_to_menu),
        migrations.AlterField(
            model_name='plato',
            name='categoria',
            field=models.CharField(
                choices=[('entrada', 'Entrada'), ('fondo', 'Fondo'), ('extra', 'Plato Extra')],
                max_length=10,
            ),
        ),
    ]
