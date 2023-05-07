import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='os_bedtime',
    version='0.0.1',
    author='Koen van der Wolf',
    author_email='holandsoest@gmail.com',
    description='Put your computer to sleep, etc.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Holandsoest/os_bedtime',
    project_urls = {
        "Bug Tracker": "https://github.com/Holandsoest/os_bedtime/issues"
    },
    license='MIT',
    packages=['os_bedtime'],
    install_requires=['psutil'],
)