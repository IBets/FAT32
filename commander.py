from file_system import LogicalDisk
import string_cfg as STR_COMMANDER
import argparse
import re


class Splitter:
    DEL_SYMBOL = 0
    DEL_EXPRESSION = 1
    NONE = 2
    REGEX = [(re.compile(r"['][ ()a-zA-Z0-9а-яА-Я_.-]*[']"), DEL_SYMBOL),
             (re.compile(r'["][ ()a-zA-Z0-9а-яА-Я_.-]*["]'), DEL_SYMBOL),
             (re.compile(r'\s+'), DEL_EXPRESSION),
             (re.compile(r'[()a-zA-Z0-9а-яА-Я_.-]+'), NONE)]

    def __init__(self, str_in):
        self.current_pos = 0
        self.str = str_in

    def read(self):
        result = []
        while self.current_pos < len(self.str):
            s = self._match_max(self.str[self.current_pos:])
            if s != '':
                result.append(s)
        return result

    def _match_max(self, str_in):
        max_str = ''
        modify = False
        for e in Splitter.REGEX:
            match = e[0].match(str_in)
            if match is not None:
                text = match.group()
                if len(text) > len(max_str):
                    max_str = text
                    modify = e[1]
        if len(max_str) > 0:
            self.current_pos += len(max_str)
        else:
            self.current_pos += len(str_in)
        if modify == Splitter.DEL_SYMBOL:
            return  max_str[1:-1]
        elif modify == Splitter.DEL_EXPRESSION:
            return ''
        else:
            return max_str


class Commander:
    def __init__(self, file_name):

        self.disk = LogicalDisk(file_name)
        self.current_directory = self.disk.root

        self.CURRENT_DIRECTORY_STR = "~/"
        self.COMMAND = {"dir": self.command_dir,
                        "info": self.command_info,
                        "cd": self.command_cd,
                        "cat": self.command_cat}

        self.KEY_INFO = {"b": lambda: print(self.disk.boot_entry),
                         "f": lambda: print(self.disk.fs_info)}

        self.KEY_CAT = {"utf-8": lambda _: _.decode("utf-8"),
                        "cp1251": lambda _: _.decode("cp1251"),
                        "ascii": lambda _: _.decode("ascii"),
                        "bin":lambda _: _}

        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(dest="command")
        subparsers.add_parser('dir')
        subparsers.add_parser('info').add_argument('-p', '--param')
        subparsers.add_parser('cd').add_argument('name')

        cat_parser = subparsers.add_parser('cat')
        cat_parser.add_argument('name')
        cat_parser.add_argument('-e', '--encoding')

    def command_dir(self, args):
        for e in self.current_directory:
            print(e)

    def command_info(self, args):
        self.KEY_INFO[args.param]()

    def command_cd(self, args):

        SEPARATE = '/'
        flag = False
        for e in self.current_directory:
            if e.name == args.name and e.is_dir():
                self.current_directory = self.disk.read_dir(e.directory_entry)
                if e.name == '..':
                    split_str = self.CURRENT_DIRECTORY_STR.split(SEPARATE)[:-2]
                    self.CURRENT_DIRECTORY_STR = ''
                    for str_e in split_str:
                        self.CURRENT_DIRECTORY_STR += (str_e + SEPARATE)
                elif e.name == '.':
                    pass
                else:
                    self.CURRENT_DIRECTORY_STR += (e.name + SEPARATE)
                flag = True
                break
        if not flag:
            print(STR_COMMANDER.COMMANDER.ERROR_CD_NOT_FOUND, args.name)

    def command_cat(self, args):

        flag = False
        for e in self.current_directory:
            if e.name == args.name and e.is_file():
                if args.encoding in self.KEY_CAT:
                    file = self.disk.read_file(e.directory_entry, e.size)
                    print(self.KEY_CAT[args.encoding](file))
                else:
                    print(STR_COMMANDER.COMMANDER.ERROR_CAT, args.encoding)
                flag = True
                break
        if not flag:
            print(STR_COMMANDER.COMMANDER.ERROR_CAR_NOT_FOUND, args.name)

    def loop(self):
        postfix = "->"
        while True:
            input_str = input(self.CURRENT_DIRECTORY_STR + postfix)
            map_command = Splitter(input_str).read()
            try:
                namespace = self.parser.parse_args(map_command)
                self.COMMAND[namespace.command](namespace)
            except SystemExit:
                pass
            except Exception as err:
                print(err)
