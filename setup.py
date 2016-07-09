from setuptools import setup, find_packages
from goods import __version__

setup(
    name='hands_chopping',
    version=__version__,
    keywords=('taobao', 'jingdong', 'hands chopping', 'spider'),
    description='Search goods in shopping web, It\' time to chop your hands.',
    author='ecmadao',
    author_email='wlec@outlook.com',
    url='https://github.com/ecmadao/Hands-Chopping',
    packages=find_packages(),
    py_modules=['run'],
    include_package_data=True,
    platforms='any',
    install_requires=[
        'prettytable',
        'bs4',
        'selenium',
        'Click'
    ],
    entry_points={
        'console_scripts': ['goods=run:get_input']
    },
    license='MIT',
    zip_safe=False,
    classifiers=[
         'Environment :: Console',
         'Programming Language :: Python',
         'Programming Language :: Python :: 3.5',
         'Programming Language :: Python :: Implementation :: CPython'
    ]
)
