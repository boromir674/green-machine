from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='green_machine',
    version='0.1',
    description='A full stack application ...',
    long_description=readme(),
    keywords='strain, self-organizing-maps, visualization',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        # 'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Science/Research',
        ],
    # url='',
    # author='Konstantinos',
    # author_email='',
    download_url='https://github.com/boromir674/music-album-creator/archive/v0.5.3.tar.gz',
    license='GNU GPLv3',
    packages=find_packages(exclude=["*.testing", "*.tests.*", "tests.*", "tests"]),
    install_requires=[],
    include_package_data=True,
    entry_points = {
        'console_scripts': ['green-web-server=music_album_creation.create_album:main'],
    },
    # TODO use the above 2 lines of code
    # setup_requires=['pytest-runner>=2.0',],
    # tests_require=['pytest',],
    tests_require=['pytest',],
    # test_suite='',
    zip_safe=False
)
