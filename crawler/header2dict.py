def get_header():
    header = {}
    with open('header.txt') as f:
        lines = f.readlines()
        for line in lines:
            index, value = line.split(': ')
            header[index] = value.replace('\n', '')
    return header

if __name__ == "__main__":
    print(get_header())
    # print(get_header()['User-Agent'])