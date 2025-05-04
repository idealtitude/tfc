#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tfc (Template File Copy) is a small, easy, and fast terminal
utility that allows you to quickly copy any file from your Templates
foler and paste it in your working directory
"""

from typing import Any, NewType
import sys
import os
import argparse
import subprocess
import shutil
import re
import string


CommandLineArguments = NewType('CommandLineArguments', argparse.Namespace)


def get_version() -> str:
    """Retrieve the current app version from file"""
    version_string: str = "0.0.1"
    version_file: str = os.path.join(os.getcwd(), "VERSION")
    if os.path.isfile(version_file):
        version_tmp: str = ''
        with open(version_file, 'r') as fd:
            version_tmp = fd.read()
        if re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", version_tmp):
            version_string = version_tmp

    return version_string


def get_home() -> str:
    """Get the path of the uesr's HOME directory"""
    home_dir: str = ''
    home_tmp: str|None = os.getenv("HOME")
    if home_tmp is None:
        home_tmp = os.path.expanduser('~')
    home_dir = home_tmp
    return home_dir


# App infos
__app_name__          : str = "tfc"
__app_author__        : str = "stephane (aka idealtitude)"
__app_version__       : str = get_version()
__app_license__       : str = "MT108"

# Constants
EXIT_SUCCESS          : int = 0
EXIT_FAILURE          : int = 1
USER_CWD              : str = os.getcwd()
USER_HOME             : str = get_home()
# Adapt the following constant value to your actual templates directory name
TEMPLATES_FOLDER_NAME : str = "Templates"

class Templates:
    """
    @brief This class handle the representation of the Templates directory content
    """
    def __init__(self, templates_folder: str = TEMPLATES_FOLDER_NAME) -> None:
        """Constructor"""
        self.categories: dict[str, dict[str, dict[str, str]]] = {}
        self.templates_path: str = os.path.join(USER_HOME, templates_folder)

        if not os.path.exists(self.templates_path):
            raise FileNotFoundError(f"\033[91mError:\033[0m the Templates folder does not exists; expected location: {self.templates_path}")

        self._make_tree()

    def _make_tree(self) -> None:
        """Build the templates tree from the templates folder"""
        for dir_name in os.listdir(self.templates_path):
            subdir: list[str] = os.listdir(os.path.join(self.templates_path, dir_name))
            self.categories[dir_name] = {}
        
            for f in subdir:
                fpath: str = os.path.join(self.templates_path, dir_name, f)
                self.categories[dir_name][f] = {"type": self.get_file_type(fpath), "path": fpath}

    def display_tree(self, template: str) -> None:
        """Display the templates tree"""
        if template == "all":
            print(f"\033[1m~/{os.path.basename(self.templates_path)}/\033[0m")
            # Display all categories
            num_categories = len(self.categories)
            for i, (category, files) in enumerate(self.categories.items()):
                is_last_category = i == num_categories - 1
                category_prefix = "└── " if is_last_category else "├── "
                print(f"{category_prefix}\033[1m{category}/\033[0m")
                num_files = len(files)
                for j, (filename, details) in enumerate(files.items()):
                    is_last_file = j == num_files - 1
                    file_prefix = "└── " if is_last_file else "├── "
                    indentation = "    " if is_last_category else "│   "
                    print(f"{indentation}{file_prefix}\033[94m{filename}\033[0m\t({details['type']})")
        elif template in self.categories:
            # Display a specific category
            print(f"\033[1m~/{os.path.basename(self.templates_path)}/{template}/\033[0m")
            num_files = len(self.categories[template])
            for i, (filename, details) in enumerate(self.categories[template].items()):
                is_last_file = i == num_files - 1
                file_prefix = "└── " if is_last_file else "├── "
                print(f"{file_prefix}\033[94m{filename}\033[0m\t({details['type']})")
        else:
            print(f"\033[91mError:\033[0m Template category '{template}' not found.")
    
    def get_file_type(self, f: str) -> str:
        """Get the file type using the `file` command with subprocess"""
        cmd = ["file", "--mime-type", "-b", f]
        try:
            result: subprocess.CompletedProcess = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"\033[91mError:\033[0m failed to get the file type: {result.stderr}")
                return "unknown"
            return result.stdout.strip()
        except FileNotFoundError as ex:
            print(f"\033[91mError:\033[0m failed to get the file type: {ex}")
            return "unknown"
        except subprocess.CalledProcessError as ex:
            print(f"\033[91mError:\033[0m failed to get the file type: {ex}")
            return "unknown"
        except Exception as ex:
            print(f"\033[91mError:\033[0m failed to get the file type: {ex}")
            return "unknown"
        return "unknown"

    # Cleaning project name
    def clean_project_name(self, project_name: str) -> str:
        """Cleaning the project name to avoid unwanted characters"""
        clean_name = project_name.strip()
        clean_name = clean_name.replace(' ', '_')
        authorized_chars = [*string.ascii_letters, *string.digits, '-', '_']
        for letter in clean_name:
            if letter not in authorized_chars:
                clean_name.replace(letter, '')
        return clean_name

    def do_copy(self, tpl: str, name: str) -> bool:
        """Actually copying the template file, from source to destination"""
        name = self.clean_project_name(name)
        src: str | None = None
        for category, files in self.categories.items():
            if tpl in files:
                src = files[tpl]['path']
                break

        if src is None:
            print(f"\033[91mError:\033[0m Template '{tpl}' not found.")
            return False

        dest: str = os.path.join(USER_CWD, name)
        try:
            shutil.copyfile(src, dest)
            print(f"\033[92mSuccess:\033[0m copied:\n{src}\nto:\n{dest}")
            return True
        except FileExistsError as ex:
            print(f"\033[91mError:\033[0m File '{name}' already exists in the current directory: {ex}")
            return False
        except Exception as ex:
            print(f"\033[91mError:\033[0m Failed to copy '{src}' to '{dest}': {ex}")
            return False


# Command line arguments
def get_args() -> CommandLineArguments:
    """Parsing command line arguments"""
    parser: Any = argparse.ArgumentParser(
        prog=f"{__app_name__}", description="Quickly and easily copy files from the Templates folder", epilog=f"Do {__app_name__} -h to display the help message"
    )

    parser.add_argument("type", nargs='?', help="The type of the file to copy")
    parser.add_argument("name", nargs='?', help="Name of the new file")
    parser.add_argument("-t", "--templates", action="store_true", help="List all available templates")
    parser.add_argument("-c", "--category", nargs=1, help="List all available templates in a specific category")
    parser.add_argument("-p", "--path", nargs=1, help="Specify the location where to copy the file; default: current working directory")
    parser.add_argument("-V", "--verbose", action="store_true", help="Display verbose output")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__app_version__}", help="Display the version number")

    return parser.parse_args()


def main(arguments: list[str]) -> int:
    """Entry point, main function."""
    if len(arguments) == 1:
        print(f"\033[91mError:\033[0m missing argument(s); do `{__app_name__}` --help to display the help message")
        return EXIT_FAILURE

    args: CommandLineArguments = get_args()

    templates = Templates()

    if len(templates.categories) == 0:
        print("\033[91mError:\033[0m while retreiving categories; the templates folder is empty")
        return EXIT_FAILURE

    if args.type and args.name:
        templates.do_copy(args.type, args.name)
    elif args.templates:
        templates.display_tree("all")
    elif args.category:
        if args.category[0] not in templates.categories:
            print(f"\033[91mError:\033[0m the template '{args.category[0]}' does not exists")
            return EXIT_FAILURE
        templates.display_tree(args.category[0])
    
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main(sys.argv))
