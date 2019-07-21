from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='redditkeys',
    version='0.1.0',
    description='Get new post from subreddits live or last as needed',
    long_description=readme,
    author='Ricardo Guevara',
    author_email='fuzztkd@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['requests', 'praw'],
    entry_points={
        'console_scripts': [
            'redditkeys=redditkeys.cli:main',
        ]
    }
)
