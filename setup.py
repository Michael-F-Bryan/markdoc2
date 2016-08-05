from setuptools import setup


setup(
        name='markdoc2',
        author='Michael F Bryan',
        author_email='michaelfbryan@gmail.com',
        version='0.1.0',
        license='MIT',

        packages=['markdoc2'],

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
