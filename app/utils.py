import logging
from PIL import Image
from PIL.ExifTags import Base, GPS, Interop, IFD, LightSource, TAGS, GPSTAGS
import click

logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s:%(message)s',
)


def get_tag(tag):
    return TAGS.get(tag, GPSTAGS.get(tag, tag))


def show_exif_data(img_path):
    try:
        img = Image.open(img_path)
        exif = img.getexif()
        if exif is not None:
            exif_str = []
            for t, v in exif.items():
                tag = get_tag(t)
                exif_str.append(f"{tag:25}: {v}")
            click.echo("\n".join(exif_str))
        else:
            click.echo("No EXIF data found.")
    except Exception as e:
        click.echo(f"Error reading EXIF data: {e}")
        logging.error(f"Error reading EXIF data: {e}")
