# Generated by Django 2.1.7 on 2019-03-27 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(db_index=True, max_length=20, unique=True)),
                ('email', models.EmailField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SolvedHiddenPuzzle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puzzle', models.CharField(choices=[('rot13', 'rot13'), ('sky', 'sky'), ('image', 'image'), ('terminal', 'terminal'), ('redirect', 'redirect'), ('login', 'login'), ('pages', 'pages'), ('audio_spectrum', 'audio_spectrum'), ('keypad', 'keypad'), ('vigenere', 'vigenere'), ('stego_mix', 'stego_mix'), ('reverse', 'reverse'), ('finish', 'finish')], max_length=40)),
                ('timestamp', models.DateTimeField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SolvedPuzzle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puzzle', models.CharField(choices=[('rot13', 'rot13'), ('sky', 'sky'), ('image', 'image'), ('terminal', 'terminal'), ('redirect', 'redirect'), ('login', 'login'), ('pages', 'pages'), ('audio_spectrum', 'audio_spectrum'), ('keypad', 'keypad'), ('vigenere', 'vigenere'), ('stego_mix', 'stego_mix'), ('reverse', 'reverse'), ('finish', 'finish')], max_length=40)),
                ('timestamp', models.DateTimeField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterIndexTogether(
            name='solvedpuzzle',
            index_together={('player', 'puzzle')},
        ),
        migrations.AlterIndexTogether(
            name='solvedhiddenpuzzle',
            index_together={('player', 'puzzle')},
        ),
    ]
