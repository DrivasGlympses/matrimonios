from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_event_latitude_event_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='linked_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plus_ones', to='core.guest'),
        ),
    ]
