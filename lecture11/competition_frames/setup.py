from setuptools import find_packages, setup

package_name = 'competition_frames'

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
    description='Lecture 11 coordinate frames and TF2: robotics competition',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'goal_broadcaster = competition_frames.goal_broadcaster:main',
            'frame_listener = competition_frames.frame_listener:main',
            'tf_go_to_goal = competition_frames.tf_go_to_goal:main',
        ],
    },
)
