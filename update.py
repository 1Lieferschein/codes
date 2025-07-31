import os
import csv
from os import listdir
from os.path import isfile, join


def compileList(dir: str):
    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    listname = os.path.basename(os.path.normpath(dir))
    mainfile = "en.csv"
    if not mainfile in files:
        print("Error: Skipped " + listname + " as en.csv file is missing!")
        return

    # make sure english is processed first
    files.remove(mainfile)
    files.insert(0, mainfile)

    header = "code"
    codes = {}

    for file in files:
        if not file.endswith(".csv"):
            print("Error: Ignoring non csv file " + file + "!")
            continue

        f = dir + "/" + file
        with open(f, 'r') as fd:
            reader = csv.reader(fd, delimiter=';', quotechar='"')
            first = True
            lang = os.path.splitext(os.path.basename(f))[0]
            mainlang = lang == os.path.splitext(os.path.basename(mainfile))[0]

            if not lang in allowedLanguages:
                print("Error: Ignoring file " + f + " as lanuage code is not in " + languageFile + "!")
                continue

            for row in reader:
                if first:
                    if row != ['CODE', 'NAME', 'DESCRIPTION']:
                        print("Warning: Ignoring file " + f + " as expected csv header is missing!")
                        break
                    header += ";" + lang + ";" + lang + "_desc"
                    first = False
                    continue

                code = row[0].strip() if 0 < len(row) else None
                name = row[1].strip() if 1 < len(row) else ""
                desc = row[2].strip() if 2 < len(row) else ""

                if code == None:
                    print("Ignoring row " + row)
                    continue

                if not code in codes:
                    if not mainlang:
                        print("Warning: Ignoring translation for " + code + " in " + lang + " for " + listname + " as code is not included in " + mainfile + "")
                        continue

                if code in codes and mainlang:
                    print("Error: Ignoring duplicate code entry in mainlang for " + code + " in " + lang + " for " + listname)
                    continue

                if code not in codes:
                    codes[code] = ""
                codes[code] += ";" + name + ";" + desc

    codes = dict(sorted(codes.items()))
    f = open(outputDir + "/" + listname + ".csv", "a")
    f.write(header + "\n")
    for c, v in codes.items():
        f.write(c + v + "\n")
    f.close()


outputDir ="out"
inputDir = "src"
languageFile = "allowed_languages.txt"

# delete previous generated output
for file in os.scandir(outputDir):
    if file.name.endswith(".csv"):
        os.unlink(file.path)

# read allowed lanugaes
allowedLanguages = []
with open(languageFile, 'r') as lf:
    allowedLanguages = lf.read().splitlines()

os.walk(inputDir)
dirs = [x[0] for x in os.walk(inputDir)]
for list in dirs[1:]:
    compileList(list)
