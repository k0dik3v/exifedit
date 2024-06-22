import logging
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import click

logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s:%(message)s',
)


def get_all_tags():
    all_tags = {}
    all_tags.update(TAGS)
    all_tags.update(GPSTAGS)
    return all_tags


def get_tag(tag, all_tags):
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
        return "No GPS data found."

    gps_data = {}

    for k in gps_info:
        decode = GPSTAGS.get(k, k)
        gps_data[decode] = gps_info[k]

    _lat = gps_data.get('GPSLatitude')
    _lat_ref = gps_data.get('GPSLatitudeRef')
    _lon = gps_data.get('GPSLongitude')
    _lon_ref = gps_data.get('GPSLongitudeRef')

    if _lat and _lat_ref and _lon and _lon_ref:
        lat = convert_to_degrees(_lat)
        if _lat_ref != "N":
            lat = -lat

        lon = convert_to_degrees(_lon)
        if _lon_ref != "E":
            lon = -lon

        return f"Latitude: {lat}, Longitude: {lon}"
    return "No GPS data found."


def show_exif_data(img_path):
    all_tags = get_all_tags()
    try:
        img = Image.open(img_path)
        exif = img.getexif()

        if exif is not None:
            exif_str = []
            for t, v in exif.items():
                tag = get_tag(t, all_tags)
                exif_str.append(f"{tag:25}: {v}")

            gps_info_str = get_gps_info(exif)
            exif_str.append(gps_info_str)

            click.echo("\n".join(exif_str))
        else:
            click.echo("No EXIF data found.")
    except Exception as e:
        click.echo(f"Error reading EXIF data: {e}")
        logging.error(f"Error reading EXIF data: {e}")
