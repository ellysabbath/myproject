# Generated by Django 5.1.6 on 2025-03-11 18:17

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('mobile_number', models.CharField(max_length=15)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('date_join', models.DateField()),
                ('date_leave', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='AmoMipangokazi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mpangokazi', models.CharField(max_length=255)),
                ('tarehe_ya_kupanga', models.DateField()),
                ('wahusika', models.CharField(max_length=255)),
                ('gharama', models.DecimalField(decimal_places=2, max_digits=10)),
                ('namna', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='AmoTaarifa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mpangokazi_done', models.CharField(max_length=255, verbose_name='Mpangokazi')),
                ('ufanisi', models.CharField(choices=[('ulitekelezwa', 'Utekelezwa'), ('haukutekelezwa', 'Haukutekelezwa')], default='ulitekelezwa', max_length=50, verbose_name='Ufanisi')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Cost')),
                ('sababu', models.TextField(verbose_name='Sababu za Kufanikiwa au La')),
                ('ushauri', models.TextField(verbose_name='Ushauri/Mapendekezo')),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('total', models.IntegerField()),
                ('abled', models.IntegerField()),
                ('disabled', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BankCashReconciliation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateOfBankTransaction', models.DateField()),
                ('dateOfCashTransaction', models.DateField()),
                ('bankDeposit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cashDeposit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('bankWithdrawal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cashWithdrawals', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('reason', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CashBudgetRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(max_length=7)),
                ('incomesource', models.CharField(max_length=255)),
                ('incomeAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expenseCategory', models.CharField(max_length=255)),
                ('expenseAmount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ElderInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('mobile_number', models.CharField(max_length=15)),
                ('username', models.CharField(max_length=255)),
                ('date_join', models.DateField()),
                ('date_leave', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='MipangokaziHazina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=7)),
                ('aim', models.CharField(max_length=255)),
                ('cost', models.CharField(max_length=255)),
                ('experts', models.CharField(max_length=255)),
                ('method', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ReceiptsPerIndividual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateindividual', models.DateField()),
                ('username', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('direction', models.CharField(max_length=255)),
                ('confirmationStatus', models.CharField(max_length=50)),
                ('leaderName', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('city', models.CharField(max_length=100)),
                ('church', models.CharField(max_length=100)),
                ('baptism_status', models.CharField(max_length=10)),
                ('gender', models.CharField(max_length=6)),
                ('password', models.CharField(max_length=100)),
                ('terms_agreement', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tithes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('date', models.CharField(max_length=20)),
                ('matoleo_type', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('amount', models.CharField(max_length=100)),
                ('direction', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile_number', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('cv_text', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cvs', to='accounts.elderinfo')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mpangokazi_done', models.CharField(max_length=255)),
                ('ufanisi', models.CharField(max_length=255)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sababu', models.TextField()),
                ('ushauri', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='accounts.elderinfo')),
            ],
        ),
        migrations.CreateModel(
            name='OtpToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_code', models.CharField(default='dc9da6', max_length=6)),
                ('tp_created_at', models.DateTimeField(auto_now_add=True)),
                ('otp_expires_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otps', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='user_images/%Y/%m/%d/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mpangokazi', models.CharField(max_length=255)),
                ('tarehe_ya_kupanga', models.DateField()),
                ('wahusika', models.CharField(max_length=255)),
                ('gharama', models.DecimalField(decimal_places=2, max_digits=10)),
                ('namna', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_plans', to='accounts.elderinfo')),
            ],
        ),
    ]
