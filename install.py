import sys
import subprocess

_all_ = ["rich>=10.7.0",
         "click>=8.0.1"]

windows = ["keyboard>=0.13.5"]

linux = ["pynput>=1.7.3"]


def install(packages):
    for package in packages:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package])


if __name__ == '__main__':

    install(_all_)
    if sys.platform == 'win32':
        install(windows)
    elif sys.platform.startswith('linux'):
        install(linux)
