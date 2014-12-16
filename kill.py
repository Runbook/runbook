import os

TEXT_FILE = 'pid.txt'


def get_pids_from_text_file():
    with open(TEXT_FILE, "rt") as f:
        data = [int(line) for line in f.readlines()]
    return data


def kill_all_pids(all_data):
    for pid in all_data:
        os.system("kill {0}".format(pid))


def main():
    all_data = get_pids_from_text_file()
    kill_all_pids(all_data)


if __name__ == '__main__':
    main()
