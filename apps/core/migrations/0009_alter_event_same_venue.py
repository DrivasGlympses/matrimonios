from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_event_ceremony_celebration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='same_venue',
            field=models.BooleanField(default=False, verbose_name='Mismo lugar para ceremonia y celebración'),
        ),
    ]
