import os
from distutils.command.build_py import build_py
from setuptools import setup
from shutil import copyfile
import subprocess

with open(os.path.join(os.path.dirname(__file__),
                       'VERSION')) as f:
    version = f.read().strip()


def download_db():
    subprocess.call(['./download.sh'])


class my_build_py(build_py):
    def run(self):
        build_py.run(self)

        if not self.dry_run:
            # Downlaod DB and copy it to the lib folder so it is later installed with the rest
            download_db()
            target_dir = os.path.join(self.build_lib)

            path = '_geoip_geolite2/GeoLite2-City.mmdb'
            copyfile(path, os.path.join(target_dir, path))


setup(
    name='python-geoip-geolite2',
    author='Armin Ronacher',
    author_email='armin.ronacher@active-4.com',
    version=version,
    url='http://github.com/mitsuhiko/python-geoip',
    packages=['_geoip_geolite2'],
    description='Provides access to the geolite2 database.  This product '
        'includes GeoLite2 data created by MaxMind, available from '
        'http://www.maxmind.com/',
    install_requires=['python-geoip'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
    ],
    cmdclass={
        'build_py': my_build_py
    }
)
