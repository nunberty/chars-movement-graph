# Translate fb2 format to correct xml tree format for parsing
import sys

def translate(data):
    data = data.split("xmlns")
    ret = data[0]
    for part in data[1:]:
        if not part[0] == ":":
            ret += "xmlns:xhtml" + part
        else:
            ret += "xmlns" + part
    return ret

def prepare_file(filename):
    with open(filename) as wrong_fb2:
        data = wrong_fb2.read()

    correct_data = translate(data)
    with open(filename, "w") as correct_fb2:
            correct_fb2.write(correct_data)

if __name__ == "__main__":
    filename = sys.argv[1]
    prepare_file(filename)
