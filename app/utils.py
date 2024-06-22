import logging
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import click

logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s:%(message)s",
)


def get_all_tag_names():
    all_tags = {}
    all_tags.update(TAGS)
    all_tags.update(GPSTAGS)
    return all_tags


def get_tag_name(tag, all_tags):
    return all_tags.get(tag, f"Unknown tag: {tag}")


def get_exif(file_name):
    image = Image.open(file_name)
    return image.getexif()


def get_geo(exif):
    for k, v in TAGS.items():
        if v == "GPSInfo":
            gps_info_key = k
            break
    else:
        return None

    gps_info = exif.get_ifd(gps_info_key)
    return {GPSTAGS.get(k, k): v for k, v in gps_info.items()} if gps_info else None


def display_exif_data(image_path):
    all_tags = get_all_tag_names()
    try:
        exif_data = get_exif(image_path)

        if exif_data:
            exif_strings = []
            for t, v in exif_data.items():
                tag_name = get_tag_name(t, all_tags)
                if tag_name == "GPSInfo":
                    exif_strings.append(f"{tag_name:25}: {v}")
                    gps_data = get_geo(exif_data)
                    if gps_data:
                        for gps_k, gps_v in gps_data.items():
                            gps_tag_name = get_tag_name(gps_k, all_tags)
                            exif_strings.append(f"{gps_tag_name:25}: {gps_v}")
                    else:
                        exif_strings.append("No GPS data found!")
                else:
                    exif_strings.append(f"{tag_name:25}: {v}")
            click.echo("\n".join(exif_strings))
        else:
            click.echo("No EXIF data found!")
    except Exception as e:
        click.echo(f"Error reading EXIF data: {e}")
        logging.error(f"Error reading EXIF data from {image_path}: {e}")
