# Wallpaper Downloader

Wallpaper Downloader - это утилита командной строки для скачивания обоев с сайта [Smashing Magazine](https://www.smashingmagazine.com/) по заданным разрешению экрана, году и месяцу.

## Установка

1. Клонируйте репозиторий:

```sh
git clone https://github.com/RedHotChilliHead/ostrovok-tech.git
cd ostrovok-tech
```
2. Создайте виртуальное окружение и активируйте его:
```sh
python -m venv venv
source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
```
3. Установите зависимости:
```sh
pip install -r requirements.txt
```
## Использование
Запуск утилиты осуществляется с помощью команды:
```sh
python downloader.py --resolution <RESOLUTION> --year <YEAR> --month <MONTH>
```

Например, для скачивания обоев с разрешением 1920x1080 за май 2024 года:
```sh
python downloader.py --resolution=1920x1080 --month=05 --year=2024
```

Скачанные обои появятся в директории ostrovok-tech/Wallpaper_05_2024.
### Аргументы
- --resolution, -r (обязательный): Разрешение экрана, например: 1920x1080
- --year, -y (обязательный): Год между 2011 и текущим годом
- --month, -m (обязательный): Месяц в числовом формате, например: 12