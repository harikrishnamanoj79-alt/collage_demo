from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdmissionInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=30)),
                ('city', models.CharField(blank=True, max_length=120)),
                ('program_interest', models.CharField(max_length=150)),
                ('current_qualification', models.CharField(blank=True, max_length=150)),
                ('message', models.TextField(blank=True)),
                ('is_reviewed', models.BooleanField(default=False)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Admission Inquiry',
                'verbose_name_plural': 'Admission Inquiries',
                'ordering': ['-submitted_at'],
            },
        ),
        migrations.CreateModel(
            name='UpcomingEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(blank=True, help_text='e.g. Workshop, Seminar, Fest', max_length=100)),
                ('event_date', models.DateField()),
                ('event_time', models.CharField(blank=True, help_text='e.g. 10:00 AM - 1:00 PM', max_length=100)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('summary', models.TextField(help_text='Short event description for the home page', max_length=400)),
                ('cta_text', models.CharField(blank=True, default='Learn More', max_length=80)),
                ('cta_link', models.CharField(blank=True, help_text='Optional internal or external link', max_length=200)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Upcoming Event',
                'verbose_name_plural': 'Upcoming Events',
                'ordering': ['display_order', 'event_date', 'title'],
            },
        ),
    ]
