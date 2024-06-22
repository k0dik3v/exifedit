import logging
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import click

logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s:%(message)s',
)


def get_all_tag_names():
    all_tags = {}
    all_tags.update(TAGS)
    all_tags.update(GPSTAGS)
    return all_tags


def get_tag_name(tag, all_tags):
    return all_tags.get(tag, f"Unknown tag {tag}")


def convert_to_degrees(value):
    d, m, s = value
    degress = d[0] / d[1]
    minutes = m[0] / m[1] / 60.0
    seconds = s[0] / s[1] / 3600.0
    return degress + minutes + seconds


def get_gps_info(exif_data):
    gps_info = exif_data.get(34853)

    if not gps_info:
        return "No GPS data."


def show_exif_data(img_path):
    all_tags = get_all_tag_names()
    try:
        img = Image.open(img_path)
        exif = img.getexif()

        if exif is not None:
            exif_str = []
            for t, v in exif.items():
                tag = get_tag_name(t, all_tags)
                if tag_name == "GPSInfo":
                    gps_info_str
                exif_str.append(f"{tag:25}: {v}"): w
                : w

            gps_info_str = get_gps_info(exif)
            exif_str.append(gps_info_str)

            click.echo("\n".join(exif_str))
        else:
            click.echo("No EXIF data found.")
    except Exception as e:
        click.echo(f"Error reading EXIF data: {e}")
        logging.error(f"Error reading EXIF data: {e}")
