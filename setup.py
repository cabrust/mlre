from distutils import util

import setuptools

main_ns = {}
ver_path = util.convert_path('mlre/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setuptools.setup(
    name="mlre",
    version=main_ns['__version__'],
    author="Clemens-Alexander Brust",
    author_email="ikosa.de@gmail.com",
    description="Machine Learning Research Environment",
    url="https://github.com/cabrust/mlre",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=["requests==2.22.0", "Flask==1.1.1"]
)
