
# setuptools import
from setuptools import setup, find_packages

setup(name="django-openmockup",
      version="0.1",
      description="Mockup application for Django",
      long_description="""
      """,
      author="Pigout Florent",
      author_email="florent.pigout@bewype.org",
      url="http://www.openmockup.org",
      install_requires = [
        "django",
        "pillow",
        "south",
        "django-userena"
      ],
      packages = find_packages(),
      include_package_data=True,
      zip_safe=False,
      classifiers = ["Development Status :: 4 - Beta",
                     "Environment :: Web Environment",
                     "Framework :: Django",
                     "Intended Audience :: Developers",
                     "License :: OSI Approved :: BSD License",
                     "Operating System :: OS Independent",
                     "Programming Language :: Python",
                     "Topic :: Utilities"],
      )
