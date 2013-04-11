#!/usr/bin/python

import os
from distutils.version import LooseVersion

SUFFIXES = ['tar', 'gz', 'sig', 'tgz']

RELEASE_TEMPLATE = """
<dt>{name}-{version}</dt>
<dd>
  <a href="releases/{filename}">{filename}</a>
</dd>
<dd>
  <a href="releases/{filename}.sig">{filename}.sig</a>
</dd>
"""


def version_rec(part):
    split = part.rsplit('.', 1)
    if len(split) == 2 and split[1] in SUFFIXES:
        part = version_rec(split[0])
    return part


def version(name):
    parts = name.rsplit('-', 1)
    if len(parts) == 2:
        return version_rec(parts[1])
    return version_rec(parts[0])


def name(file):
    return file.rsplit('-', 1)[0]


def main():
    template = open('releases.html.in', 'r').read()

    files = os.listdir('releases')
    files = [file for file in files if file.endswith('.sig') and
             file[:-4] in files]
    files.sort(key=lambda s: LooseVersion(version(s)))
    files.reverse()

    releases = ""

    for file in files:
        releases += RELEASE_TEMPLATE.format(filename=file[:-4],
                                            name=name(file),
                                            version=version(file))

    content = template.replace('{{RELEASES}}', releases)

    output = open('releases.html', 'w')
    output.write(content)
    output.close()

if __name__ == '__main__':
    main()
