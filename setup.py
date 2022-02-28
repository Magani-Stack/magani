from setuptools import setup

with open("README.md", "r") as readme:
    description = readme.read()

with open("LICENSE", "r") as readme:
    license_x = readme.read()

with open("version.txt", "r") as readme:
    version_x = readme.read()

with open("requirements.txt", "r") as readme:
    install_requires = readme.read()

license_x_y = " : ".join(x for x in license_x.split("\n")[:3] if x)

description = "{} \n\n {}".format(description, license_x_y)

requirements = [
    ".",
    "magani", "assets", "magani.data.projects", "magani.http", "magani.auth", "magani.utils"
]

install_requires = [x.strip() for x in install_requires.split("\n") if x]

setup(
    name='magani',
    version=version_x,
    packages=requirements,
    url='https://github.com/Magani-Stack/magani',
    license=license_x_y,
    author='Abimanyu H K',
    author_email='manyu1994@hotmail.com',
    description='REST API testing software developed in pure Python',
    long_description=description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=install_requires,
    data_files=[("assets", ["assets/mg.jpg", "assets/favicon.ico"])],
    scripts=["script/magani.bat", "script/magani.sh"],
    package_data={
        # 'magani': ['data\projects\projects.json'],
    }
)
