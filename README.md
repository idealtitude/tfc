# tfc

**tfc** (Template File Copy) is a small, easy, and fast terminal utility that allows you to quickly copy any file from your Templates foler and paste it in your working directory

![tfc logo](./tfc.png)

## Requirements

I'm using Python 3.12; I didn't test the script with other versions.

## Install/Unintsall

### Install

Clone the repository:

```bash
git clone https://github.com/yourusername/tfc.git
cd tfc
# make the script executable
chmod +x tfc.py
```

If your Templates folder has a different name (e.g. "Modèles" in French), edit the file to change `TEMPLATES_FOLDER_NAME` to the desired value (this constant is near the top of the script):

```bash
nano tfc.py
```

"Install" the script:

Either  use the provided `Makefile`:

```bash
make
# Or:
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

### Command-Line Usage

Run the script with the following command:

```bash
tfc <template name> <file name>
```

### Options

- `--templates`: list all the available template files by their categories
- `--category`: list all available templates in a specific category
- `--path`: the location where to copy the template; default: current working directory

### Example

```bash
tfc bash bash_script.sh --path '~/Dev/BASH'
```

## TODO's

- [ ] adapt the script to handle any abritray number of folders and sub-folders; we'll be using `os.walk` for that

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
