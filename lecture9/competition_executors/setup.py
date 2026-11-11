from setuptools import find_packages, setup

package_name = 'competition_executors'

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
    description='Lecture 9 executors and callback groups: robotics competition',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'single_threaded = competition_executors.controller_runs:single_threaded',
            'multi_threaded = competition_executors.controller_runs:multi_threaded',
            'two_groups = competition_executors.controller_runs:two_groups',
            'slow_plan = competition_executors.controller_runs:slow_plan',
            'reentrant_plan = competition_executors.controller_runs:reentrant_plan',
            'battery_pair = competition_executors.battery_pair:main',
        ],
    },
)
