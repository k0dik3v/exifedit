import click
from app.utils import show_exif_data


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    '-s',
    '--show-exif',
    'img_path',
    type=click.Path(exists=True),
    help='Path to the image file to display EXIF data.'
)
def show_exif(img_path):
    if img_path:
        show_exif_data(img_path)
    else:
        click.echo(
            "No image path provided. Use the -s option to specify an image.")


if __name__ == '__main__':
    cli()
