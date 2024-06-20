from setuptools import setup, find_packages

setup(
    name='edit_exif',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'edit-exif = app.cli:hello',
        ],
    },
)
