from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ilanlar', '0005_advertisement_latitude_advertisement_longitude'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favoriler', to='ilanlar.advertisement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favoriler', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Favori',
                'verbose_name_plural': 'Favoriler',
                'ordering': ['-created_at'],
                'unique_together': {('user', 'ad')},
            },
        ),
    ]