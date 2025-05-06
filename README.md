# tfc

**tfc** stands for **T**emplate **F**ile **C**opy. It is a small, easy, and fast terminal utility that allows you to copy any file from your Templates folder and paste it in your working directory (or any other location of your choice; see the options menu with `tfc --help`).

![tfc logo](./tfc.png)

## Requirements

I'm using Python 3.12 for writing this app; I didn't test it with other versions.

## Install/Unintsall

### Install

Clone the repository:

```bash
git clone https://github.com/idealtitude/tfc.git
cd tfc
# make the script executable
chmod +x tfc.py
```

/!\ **Important**
If your Templates folder has a different name (e.g. "Modèles" in French), edit the file to change `TEMPLATES_FOLDER_NAME` to the desired value (this constant is near the top of the script):

```bash
ed -p"% " tfc.py
```

You can (and you will, probably) choose another text editor of course (unless you're a [hardcore-Unix](https://www.youtube.com/watch?v=JoVQTPbD6UY)-[early-days](https://www.youtube.com/watch?v=tc4ROCJYbm0)-[miminalism-purist](https://www.youtube.com/watch?v=XvDZLjaCJuw&t=1020s))! Ce ne sont point les choix qui manquent:

1. vim
2. neovim
3. nano
4. helix
5. [micro](https://micro-editor.github.io/ "Micro Editor Home Page") (This one is my favorite, I recommend it warmly)
6. emacs
7. [ed](https://www.redhat.com/en/blog/introduction-ed-editor)

Vous avez [l'embarras du choix](https://fr.wiktionary.org/wiki/avoir_l%E2%80%99embarras_du_choix)...


*Install* the script:

Either  use the provided `Makefile`:

```bash
make install
```

Or do it manually:

```bash
# Put it in your `~/.local.bin` folder, for example
cp tfc.py ~/.local/bin/tfc
# or make a symbolic link
ln -s /path/to/tfc/tfc.py "$HOME/.local/bin/tfc"
```

### Uninstall

Simply delete the script from where you've installed it, or use the Makefile:

```bash
make uninstall
```

## Usage

The script is primarly designed to be used directly from the command line.

[![asciicast](https://asciinema.org/a/kU9hz5C7AdrZuayORW2OPTaGj.svg)](https://asciinema.org/a/kU9hz5C7AdrZuayORW2OPTaGj)

### Command-Line Usage

Run the script with the following command:

```bash
# Copy the <template> to <name>
# tfc <template> <name>
tfc py my_script.py
```

### Options

- `--templates`: list all the available template files by their categories
- `--category` : list all available templates in a specific category
- `--path`     : the location where to copy the template; default: current working directory

### Examples

#### Dislay the list of a sub category

```bash
tfc -c html
```

#### Specify another path where to copy the file, rather the default which is your current working directory

```bash
tfc bash my_script.sh --path '~/Dev/BASH/TESTS'
```

## TODO's

- [ ] adapt the script to handle any abritray number of folders and sub-folders in the Templates root folder; we'll be using `os.walk` for that
- [ ] implement the `--verbose` option
- [ ] improve the `Makefile`

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
