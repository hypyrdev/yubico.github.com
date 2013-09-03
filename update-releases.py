#!/usr/bin/python

import os
from distutils.version import LooseVersion

SUFFIXES = ['tar', 'gz', 'sig', 'tgz', 'zip', 'cap', 'apk']
CLASSIFIERS = ['win32', 'win64', 'mac']

RELEASE_TEMPLATE = """
<dt>{name}</dt>
<dd>
  <a href="releases/{filename}">{filename}</a>
</dd>
<dd>
  <a href="releases/{filename}.sig">{filename}.sig</a>
</dd>
"""


def remove_suffixes(part):
    split = part.rsplit('.', 1)
    if len(split) == 2 and split[1] in SUFFIXES:
        part = remove_suffixes(split[0])
    return part


def remove_classifier(part):
    split = part.rsplit('-', 1)
    if len(split) == 2 and split[1] in CLASSIFIERS:
        return split[0], split[1]
    return part, None


def version(filename):
    part = remove_suffixes(filename)
    part, classifier = remove_classifier(part)
    version = part.rsplit('-', 1)[1]
    if classifier:
        return '%s-%s' % (version, classifier)
    return version


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
                                            name=remove_suffixes(file))

    content = template.replace('{{RELEASES}}', releases)

    output = open('releases.html', 'w')
    output.write(content)
    output.close()

    os.system('git add releases.html')

if __name__ == '__main__':
    main()
