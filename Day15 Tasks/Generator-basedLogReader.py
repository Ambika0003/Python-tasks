def read_file():
    with open("log.txt", "r") as f:
        for line in f:
            yield line.strip()

count = {}

for line in read_file():
    if "error" in line.lower():   # FIXED
        if line in count:
            count[line] += 1
        else:
            count[line] = 1

for key in count:
    print(key, ":", count[key])