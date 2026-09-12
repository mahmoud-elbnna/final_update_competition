import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'mia_competition'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Mahmoud Elbnna',
    maintainer_email='mahmoudalaa2022o8@gmail.com',
    description='MIA Competition ROS 2 Package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'auto_node = mia_competition.autonmous_phase:main',
            'manual_node = mia_competition.manual_phase:main',
            'select_node = mia_competition.autonmous_manual_selection:main',
        ],
    },
)