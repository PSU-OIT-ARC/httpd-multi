from setuptools import setup, find_packages


setup(
    name='psu.oit.arc.httpdmulti',
    version='1.0.dev0',
    description='Run multiple instance of Apache (httpd)',
    author='PSU - OIT - ARC',
    author_email='consultants@pdx.edu',
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
    [console_scripts]
    httpdmulti = httpdmulti.__main__:main

    """,
)
