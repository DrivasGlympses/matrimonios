from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_event_email_button_text_event_email_closing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ceremony_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Hora de la Ceremonia'),
        ),
        migrations.AddField(
            model_name='event',
            name='celebration_location',
            field=models.CharField(blank=True, max_length=300, verbose_name='Lugar de la Celebración'),
        ),
        migrations.AddField(
            model_name='event',
            name='celebration_latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitud de la Celebración'),
        ),
        migrations.AddField(
            model_name='event',
            name='celebration_longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitud de la Celebración'),
        ),
        migrations.AddField(
            model_name='event',
            name='celebration_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Hora de la Celebración'),
        ),
        migrations.AddField(
            model_name='event',
            name='celebration_venue_details',
            field=models.TextField(blank=True, verbose_name='Detalles del Lugar de la Celebración'),
        ),
        migrations.AddField(
            model_name='event',
            name='same_venue',
            field=models.BooleanField(default=True, verbose_name='Mismo lugar para ceremonia y celebración'),
        ),
        migrations.AlterField(
            model_name='event',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitud de la Ceremonia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, max_length=300, verbose_name='Lugar de la Ceremonia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitud de la Ceremonia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue_details',
            field=models.TextField(blank=True, verbose_name='Detalles del Lugar de la Ceremonia'),
        ),
    ]
