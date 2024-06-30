from setuptools import setup, find_packages

setup(
    name="crypter",
    version="1.0.0",
    author="BgRopay",
    description="Crack Linux Password with Python",
    long_description=open('README.md').read(),  # Ensure you have a README.md file
    long_description_content_type="text/markdown",
    url="https://github.com/bgropay/crypter",
    packages=find_packages(),
    py_modules=["crypter"],
    install_requires=[
        "colorama",
    ],
    entry_points={
        'console_scripts': [
            'crypter=crypter:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
