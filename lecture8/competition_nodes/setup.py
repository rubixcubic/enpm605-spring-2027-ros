from setuptools import find_packages, setup

package_name = 'competition_nodes'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Zeid Kootbally',
    maintainer_email='zeidk@umd.edu',
    description='Lecture 8 nodes: robotics competition',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'minimal_node = competition_nodes.minimal_node:main',
            'scout_node = competition_nodes.scout_node:main',
            'heartbeat_node = competition_nodes.heartbeat_node:main',
            'battery_publisher = competition_nodes.battery_publisher:main',
            'battery_monitor = competition_nodes.battery_monitor:main',
        ],
    },
)
