from glob import glob

from setuptools import find_packages, setup

package_name = 'competition_nav'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*')),
        ('share/' + package_name + '/worlds', glob('worlds/*')),
        ('share/' + package_name + '/maps', glob('maps/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Zeid Kootbally',
    maintainer_email='zeidk@umd.edu',
    description='Lecture 12 mapping and navigation: robotics competition',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'route_driver = competition_nav.route_driver:main',
            'grid_reader = competition_nav.grid_reader:main',
            'cost_probe = competition_nav.cost_probe:main',
            'initial_pose = competition_nav.initial_pose:main',
            'amcl_watch = competition_nav.amcl_watch:main',
            'nav_client = competition_nav.nav_client:main',
        ],
    },
)
