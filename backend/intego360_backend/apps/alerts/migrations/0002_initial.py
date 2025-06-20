# Generated by Django 5.2.1 on 2025-06-03 20:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alerts', '0001_initial'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alert_actions', to='authentication.user'),
        ),
        migrations.AddField(
            model_name='alertnotification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alert_notifications', to='authentication.user'),
        ),
        migrations.AddField(
            model_name='alertrule',
            name='auto_assign_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auto_assigned_alerts', to='authentication.user'),
        ),
        migrations.AddField(
            model_name='alertrule',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_alert_rules', to='authentication.user'),
        ),
        migrations.AddField(
            model_name='alertsubscription',
            name='districts',
            field=models.ManyToManyField(blank=True, related_name='alert_subscribers', to='authentication.district'),
        ),
        migrations.AddField(
            model_name='alertsubscription',
            name='sectors',
            field=models.ManyToManyField(blank=True, related_name='alert_subscribers', to='authentication.sector'),
        ),
        migrations.AddField(
            model_name='alertsubscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alert_subscriptions', to='authentication.user'),
        ),
        migrations.AddField(
            model_name='alertsubscription',
            name='alert_types',
            field=models.ManyToManyField(related_name='subscribers', to='alerts.alerttype'),
        ),
        migrations.AddField(
            model_name='alertrule',
            name='alert_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='alerts.alerttype'),
        ),
        migrations.AddField(
            model_name='systemalert',
            name='alert_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to='alerts.alerttype'),
        ),
        migrations.AddField(
            model_name='systemalert',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_alerts', to='authentication.user'),
        ),
        migrations.AddField(
            model_name='systemalert',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_alerts', to='authentication.user'),
        ),
        migrations.AddField(
            model_name='systemalert',
            name='districts',
            field=models.ManyToManyField(blank=True, related_name='system_alerts', to='authentication.district'),
        ),
        migrations.AddField(
            model_name='systemalert',
            name='resolved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resolved_alerts', to='authentication.user'),
        ),
        migrations.AddField(
            model_name='systemalert',
            name='sectors',
            field=models.ManyToManyField(blank=True, related_name='system_alerts', to='authentication.sector'),
        ),
        migrations.AddField(
            model_name='alertnotification',
            name='alert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='alerts.systemalert'),
        ),
        migrations.AddField(
            model_name='alertaction',
            name='alert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='alerts.systemalert'),
        ),
        migrations.AddIndex(
            model_name='systemalert',
            index=models.Index(fields=['status', 'severity'], name='alerts_syst_status_23a219_idx'),
        ),
        migrations.AddIndex(
            model_name='systemalert',
            index=models.Index(fields=['created_at', 'priority_score'], name='alerts_syst_created_9ddd58_idx'),
        ),
        migrations.AddIndex(
            model_name='systemalert',
            index=models.Index(fields=['alert_type', 'status'], name='alerts_syst_alert_t_5da1ac_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='alertnotification',
            unique_together={('alert', 'user', 'notification_type')},
        ),
    ]
