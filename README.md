# hackthespace

## Dependencies

* Python 3.5+ (dev package)
* GCC, G++
* ffmpeg
* taglib (dev package)

Debian:
```
sudo apt install python3 python3-dev gcc g++ ffmpeg libtag1-dev
```

## Quick Start

```
pip install -r requirements.txt
cp hackthespace/settings/local_settings.py{.example,}
python manage.py migrate
python manage.py generate_assets
python manage.py runserver
```

## Deployment

```
python manage.py compilescss
```
