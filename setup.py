from setuptools import setup


setup(
        name='markdoc2',
        author='Michael F Bryan',
        author_email='michaelfbryan@gmail.com',
        version='0.2.0',
        license='MIT',

        packages=['markdoc2'],
        include_package_data = True,
        package_data={
            '': ['static/templates/*.html'],
            },

        install_requires=[
            'markdown',
            'jinja2',
            'docopt',
            'bs4',
            ],

        entry_points={
            'console_scripts': [
                'markdoc2=markdoc2.__main__:main',
                ],
            },
        )
