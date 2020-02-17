import setuptools

setuptools.setup(
    name="mlre",
    version="0.0.1",
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
