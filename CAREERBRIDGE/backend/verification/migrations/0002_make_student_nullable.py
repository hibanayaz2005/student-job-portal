"""Make VerificationDocument.student nullable and remove unique_together."""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationdocument',
            name='student',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.studentprofile'),
        ),
        migrations.AlterModelOptions(
            name='verificationdocument',
            options={},
        ),
    ]
