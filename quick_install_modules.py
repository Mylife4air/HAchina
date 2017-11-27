import os
import pip
import sys

from subprocess import call


def exchange():
    pip_path = sys.argv[2]
    with open(pip_path, 'r') as fs:
        for line in fs:
            if line[0] != '#':
                string = path + ' install ' + line
                os.system(string)

    package_list_str = " ".join([dist.project_name for dist in pip.get_installed_distributions()])
    com = path+'--upgrade '
    call(com + package_list_str, shell=True)


if __name__ =='__main__':
    exchange()
