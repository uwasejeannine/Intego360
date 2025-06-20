# Generated by Django 5.2.1 on 2025-06-03 20:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgricultureAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('alert_type', models.CharField(choices=[('weather', 'Weather Alert'), ('pest_disease', 'Pest/Disease Alert'), ('market', 'Market Alert'), ('input_shortage', 'Input Shortage'), ('extension', 'Extension Service'), ('policy', 'Policy Update'), ('emergency', 'Emergency')], max_length=20)),
                ('severity', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], max_length=10)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('recommended_actions', models.TextField()),
                ('resources_available', models.TextField(blank=True)),
                ('contact_person', models.CharField(max_length=100)),
                ('contact_phone', models.CharField(max_length=15)),
                ('farmers_reached', models.IntegerField(default=0)),
                ('cooperatives_notified', models.IntegerField(default=0)),
                ('actions_taken', models.TextField(blank=True)),
                ('effectiveness_score', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Agriculture Alert',
                'verbose_name_plural': 'Agriculture Alerts',
                'ordering': ['-created_at', '-severity'],
            },
        ),
        migrations.CreateModel(
            name='AgricultureExtension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('service_type', models.CharField(choices=[('training', 'Training'), ('demonstration', 'Demonstration'), ('advisory', 'Advisory Service'), ('input_supply', 'Input Supply'), ('market_linkage', 'Market Linkage'), ('technology', 'Technology Transfer')], max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('venue', models.CharField(max_length=200)),
                ('facilitator', models.CharField(max_length=100)),
                ('facilitator_organization', models.CharField(max_length=100)),
                ('target_participants', models.IntegerField()),
                ('actual_participants', models.IntegerField(default=0)),
                ('male_participants', models.IntegerField(default=0)),
                ('female_participants', models.IntegerField(default=0)),
                ('youth_participants', models.IntegerField(default=0)),
                ('budget_allocated', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('budget_spent', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('materials_provided', models.TextField(blank=True)),
                ('knowledge_gained', models.TextField(blank=True)),
                ('practices_adopted', models.TextField(blank=True)),
                ('feedback', models.TextField(blank=True)),
                ('success_rate', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('status', models.CharField(choices=[('planned', 'Planned'), ('ongoing', 'Ongoing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='planned', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Agriculture Extension',
                'verbose_name_plural': 'Agriculture Extensions',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='AgricultureTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_area_hectares', models.FloatField()),
                ('target_production_tons', models.FloatField()),
                ('target_yield_tons_per_hectare', models.FloatField()),
                ('target_farmers', models.IntegerField()),
                ('allocated_budget', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('budget_for_seeds', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('budget_for_fertilizers', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('budget_for_extension', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('achieved_area_hectares', models.FloatField(default=0.0)),
                ('achieved_production_tons', models.FloatField(default=0.0)),
                ('farmers_participating', models.IntegerField(default=0)),
                ('budget_utilized', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Agriculture Target',
                'verbose_name_plural': 'Agriculture Targets',
                'ordering': ['-season__year', 'district__name', 'crop__name'],
            },
        ),
        migrations.CreateModel(
            name='Cooperative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('registration_number', models.CharField(max_length=20, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('physical_address', models.TextField()),
                ('chairperson_name', models.CharField(max_length=100)),
                ('chairperson_phone', models.CharField(max_length=15)),
                ('secretary_name', models.CharField(blank=True, max_length=100)),
                ('treasurer_name', models.CharField(blank=True, max_length=100)),
                ('date_established', models.DateField()),
                ('total_members', models.IntegerField(default=0)),
                ('active_members', models.IntegerField(default=0)),
                ('female_members', models.IntegerField(default=0)),
                ('youth_members', models.IntegerField(default=0)),
                ('total_assets', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('annual_revenue', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('primary_activities', models.TextField(help_text='Main activities of the cooperative')),
                ('is_active', models.BooleanField(default=True)),
                ('certification_status', models.CharField(choices=[('pending', 'Pending'), ('certified', 'Certified'), ('suspended', 'Suspended'), ('revoked', 'Revoked')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cooperative',
                'verbose_name_plural': 'Cooperatives',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('scientific_name', models.CharField(blank=True, max_length=150)),
                ('category', models.CharField(choices=[('cereals', 'Cereals'), ('legumes', 'Legumes'), ('tubers', 'Tubers'), ('vegetables', 'Vegetables'), ('fruits', 'Fruits'), ('cash_crops', 'Cash Crops')], max_length=50)),
                ('growing_season', models.CharField(choices=[('season_a', 'Season A (Sep-Jan)'), ('season_b', 'Season B (Feb-Jun)'), ('season_c', 'Season C (Jul-Aug)'), ('year_round', 'Year Round')], max_length=20)),
                ('growth_period_days', models.IntegerField(help_text='Days from planting to harvest')),
                ('ideal_rainfall_mm', models.FloatField(help_text='Ideal annual rainfall in mm')),
                ('ideal_temperature_min', models.FloatField(help_text='Minimum temperature in Celsius')),
                ('ideal_temperature_max', models.FloatField(help_text='Maximum temperature in Celsius')),
                ('average_yield_per_hectare', models.FloatField(default=0.0, help_text='Average yield in tons per hectare')),
                ('market_price_per_kg', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Crop',
                'verbose_name_plural': 'Crops',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CropProduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_planted_hectares', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('planting_date', models.DateField()),
                ('seed_variety', models.CharField(blank=True, max_length=100)),
                ('seed_source', models.CharField(choices=[('own', 'Own seeds'), ('purchased', 'Purchased'), ('government', 'Government supplied'), ('cooperative', 'Cooperative supplied'), ('ngo', 'NGO supplied')], default='own', max_length=20)),
                ('fertilizer_used', models.BooleanField(default=False)),
                ('fertilizer_type', models.CharField(blank=True, max_length=100)),
                ('fertilizer_quantity_kg', models.FloatField(default=0.0)),
                ('pesticide_used', models.BooleanField(default=False)),
                ('pesticide_type', models.CharField(blank=True, max_length=100)),
                ('irrigation_used', models.BooleanField(default=False)),
                ('irrigation_type', models.CharField(blank=True, max_length=50)),
                ('harvest_date', models.DateField(blank=True, null=True)),
                ('quantity_harvested_kg', models.FloatField(default=0.0)),
                ('quality_grade', models.CharField(blank=True, choices=[('A', 'Grade A - Excellent'), ('B', 'Grade B - Good'), ('C', 'Grade C - Fair'), ('D', 'Grade D - Poor')], max_length=10)),
                ('quantity_consumed_kg', models.FloatField(default=0.0)),
                ('quantity_sold_kg', models.FloatField(default=0.0)),
                ('quantity_stored_kg', models.FloatField(default=0.0)),
                ('quantity_lost_kg', models.FloatField(default=0.0)),
                ('average_selling_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('challenges_faced', models.TextField(blank=True)),
                ('pest_diseases', models.TextField(blank=True)),
                ('weather_impact', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Crop Production',
                'verbose_name_plural': 'Crop Productions',
                'ordering': ['-season__year', '-harvest_date'],
            },
        ),
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farmer_id', models.CharField(max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('national_id', models.CharField(max_length=16, unique=True)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('cell', models.CharField(max_length=50)),
                ('village', models.CharField(max_length=50)),
                ('total_land_hectares', models.FloatField(default=0.0)),
                ('farming_experience_years', models.IntegerField(default=0)),
                ('education_level', models.CharField(choices=[('none', 'No formal education'), ('primary', 'Primary education'), ('secondary', 'Secondary education'), ('vocational', 'Vocational training'), ('university', 'University education')], default='primary', max_length=20)),
                ('is_cooperative_member', models.BooleanField(default=False)),
                ('cooperative_name', models.CharField(blank=True, max_length=100)),
                ('has_bank_account', models.BooleanField(default=False)),
                ('bank_name', models.CharField(blank=True, max_length=100)),
                ('account_number', models.CharField(blank=True, max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Farmer',
                'verbose_name_plural': 'Farmers',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='MarketPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market_name', models.CharField(max_length=100)),
                ('price_per_kg', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='RWF', max_length=3)),
                ('quality_grade', models.CharField(choices=[('A', 'Grade A'), ('B', 'Grade B'), ('C', 'Grade C'), ('mixed', 'Mixed')], default='mixed', max_length=10)),
                ('supply_level', models.CharField(choices=[('low', 'Low Supply'), ('normal', 'Normal Supply'), ('high', 'High Supply'), ('oversupply', 'Oversupply')], max_length=20)),
                ('demand_level', models.CharField(choices=[('low', 'Low Demand'), ('normal', 'Normal Demand'), ('high', 'High Demand')], max_length=20)),
                ('quantity_available_kg', models.FloatField(default=0.0)),
                ('price_trend', models.CharField(choices=[('increasing', 'Increasing'), ('stable', 'Stable'), ('decreasing', 'Decreasing')], default='stable', max_length=20)),
                ('data_source', models.CharField(choices=[('market_survey', 'Market Survey'), ('trader_report', 'Trader Report'), ('government', 'Government Data'), ('cooperative', 'Cooperative Report'), ('online', 'Online Platform')], max_length=50)),
                ('date_recorded', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Market Price',
                'verbose_name_plural': 'Market Prices',
                'ordering': ['-date_recorded', 'crop__name'],
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('season_a', 'Season A'), ('season_b', 'Season B'), ('season_c', 'Season C')], max_length=20)),
                ('year', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_rainfall_mm', models.FloatField(default=0.0)),
                ('average_temperature', models.FloatField(default=0.0)),
                ('drought_periods', models.IntegerField(default=0, help_text='Number of drought periods')),
                ('flood_incidents', models.IntegerField(default=0, help_text='Number of flood incidents')),
                ('total_production_tons', models.FloatField(default=0.0)),
                ('total_area_cultivated', models.FloatField(default=0.0)),
                ('average_yield', models.FloatField(default=0.0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Season',
                'verbose_name_plural': 'Seasons',
                'ordering': ['-year', 'name'],
            },
        ),
    ]
