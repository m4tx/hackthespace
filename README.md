# stronghold

## Quick Start

```
pip install -r requirements.txt
cp stronghold/settings/local_settings.py{.example,}
python manage.py migrate
python manage.py generate_image_assets
python manage.py generate_audio_spectrum_assets
python manage.py runserver
```
