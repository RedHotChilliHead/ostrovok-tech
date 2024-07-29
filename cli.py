import os
import logging
import click
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import aiohttp
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Возможные разрешения для проверки ввода
VALID_RESOLUTIONS = [
    '320x480', '640x480', '800x480', '800x600', '1024x768', '1024x1024', '1152x864', '1280x720',
    '1280x800', '1280x960', '1280x1024', '1400x1050', '1440x900', '1600x1200', '1680x1050', '1680x1200',
    '1920x1080', '1920x1200', '1920x1440', '2560x1440', '3840x2160'
]

MONTH_DICT = {
    '01': 'january',
    '02': 'february',
    '03': 'march',
    '04': 'april',
    '05': 'may',
    '06': 'june',
    '07': 'july',
    '08': 'august',
    '09': 'september',
    '10': 'october',
    '11': 'november',
    '12': 'december'
}


def validate_input(resolution, year, month):
    if resolution not in VALID_RESOLUTIONS:
        raise click.BadParameter(f'Invalid resolution value: {resolution}. Use one of the: {VALID_RESOLUTIONS}')

    try:
        month_int = int(month)
        if month_int < 1 or month_int > 12:
            raise ValueError
    except ValueError:
        raise click.BadParameter('Month value is not valid. Use a digit between 1 and 12.')

    try:
        year_int = int(year)
        if year_int < 2011 or year_int > datetime.now().year:
            raise ValueError
    except ValueError:
        raise click.BadParameter('Year value is not valid. Use a digit between 2011 and the current year.')


def get_url(base_url, year, month):
    month = month.zfill(2)
    if month not in MONTH_DICT:
        raise ValueError(f'Month value is not valid: {month}')

    month_name = MONTH_DICT[month]

    if month == '01':
        month_pub = '12'
        year_pub = str(int(year) - 1)
    else:
        month_pub = str(int(month) - 1).zfill(2)
        year_pub = year

    return f"{base_url}{year_pub}/{month_pub}/desktop-wallpaper-calendars-{month_name}-{year}/"


def get_links(url, resolution):
    response = requests.get(url)
    response.raise_for_status()

    root = BeautifulSoup(response.content, 'html.parser')
    el_a = root.find_all('a', string=lambda text: text and resolution in text)

    return [link.get('href') for link in el_a]


async def download_file(session, link, storage_path):
    try:
        async with session.get(link, ssl=False) as response:  # выполняет асинхронный HTTP GET-запрос
            response.raise_for_status()  # проверяем статус-код ответа и выбрасывает исключение, если статус-код не 200
            file_name = os.path.basename(link)
            file_path = os.path.join(storage_path, file_name)
            with open(file_path, 'wb') as file:
                file.write(await response.read())  # асинхронно считываем содержимое ответа и записываем его в файл
            logger.info(f'File {file_name} downloaded successfully')
    except Exception as e:
        logger.error(f'Failed to download file {link}: {e}')


async def download(links, base_dir, month, year):
    storage_path = os.path.join(base_dir, f'Wallpaper_{month}_{year}')
    os.makedirs(storage_path, exist_ok=True)  # cоздаем каталог для сохранения файлов, если он не существует

    # создаем асинхронную HTTP-сессию, которая будет использоваться для загрузки файлов
    async with aiohttp.ClientSession() as session:
        tasks = [download_file(session, link, storage_path) for link in links]  # список задач для загрузки файлов
        await asyncio.gather(*tasks)  # запускаем все задачи параллельно и ждем их завершения


@click.command()
@click.option('--resolution', '-r', required=True, help='Resolution, example: 1920x1080 [required]')
@click.option('--year', '-y', required=True, help='Year between 2011 and the current year [required]')
@click.option('--month', '-m', required=True, help='Month, number format, example: 12 [required]')
def main(resolution, year, month):
    """
    Program for downloading files from 'www.smashingmagazine.com"
    """
    validate_input(resolution, year, month)

    URL = 'https://www.smashingmagazine.com/'
    url = get_url(URL, year, month)

    try:
        links = get_links(url, resolution)
    except requests.RequestException as e:
        raise click.ClickException(f'Failed to get links: {e}')

    try:
        # запускает асинхронную функцию и блокирует выполнение до тех пор, пока она не завершится
        asyncio.run(download(links, BASE_DIR, month, year))  # вызов асинхронной функции
    except Exception as e:
        raise click.ClickException(f'Failed to download files: {e}')


if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    main()
