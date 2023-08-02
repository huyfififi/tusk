import distutils
import setuptools

import tusk

distutils.core.setup(
    name="tusk",
    version=tusk.__version__,
    description="command-line client for mastodon",
    url="https://github.com/huyfififi/tusk",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=["html2text", "requests"],
    entry_points={"console_scripts": ["tusk = tusk.tusk:main"]},
)
