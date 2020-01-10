#!python3.7

import os
import re

path = 'files/'

def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()

for r, d, f in os.walk(path):
    for folder in d:
        path_base = path + folder + '/'
        files = [os.path.join(path_base,f) for f in os.listdir(path_base) if os.path.isfile(os.path.join(path_base,f))]
        number_files = len(files)
        if number_files > 1:
            linesToAdd = ['<h1 class="calibre1" id="calibre_pb_1">Table of Contents</h1>\n','<p class="calibre6">\n']
            for x in range(number_files):
                linesToAdd.append('<a href="Chapter' + str(x) + '.html">Chapter ' + str(x) + '</a><br class="calibre5"/>\n')
            
            # read contents of file
            with open(path_base + 'Chapter0.html', 'r+') as chapter0:
                lines = chapter0.readlines()
                deleteContent(chapter0)
                for i in range(len(lines)):
                    line = lines[i]

                    if '</h3>' in line:
                        print(line)
                        line += '\n\n'
                        for line0 in linesToAdd:
                            line += line0
                        line += '\n\n'
                        lines[i] = line

                chapter0.writelines(lines)
                chapter0.close()

