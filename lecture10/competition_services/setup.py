from setuptools import find_packages, setup

package_name = 'competition_services'

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
    description='Lecture 10 services: robotics competition',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'task_server = competition_services.task_server:main',
            'task_client = competition_services.task_client:main',
            'async_requester = competition_services.task_requester:async_requester',
            'sync_requester = competition_services.task_requester:sync_requester',
            'sync_two_groups = competition_services.task_requester:sync_two_groups',
        ],
    },
)
