# PreTeXt AsciiMath to LaTeX

This project is an extension to the [**PreTeXt MathBook XML**](https://github.com/rbeezer/mathbook) project. It provides a convenient way for PreTeXt authors to convert [AsciiMath](asciimath.org) to LaTeX.

Please install **Python 2.7** and [`xsltproc`](https://mathbook.pugetsound.edu/doc/author-guide/html/quickstart-setup.html) before continuing.

## Getting started

Clone this repository. Then, clone **mathbook** repository to access `PreTeXt` source, including a sample book and article.
```shell
$ git clone https://github.com/ymittal/asciimath
$ cd asciimath
$ git clone https://github.com/rbeezer/mathbook
$ virtualenv .env && source .env/bin/activate   # (optional) setup virtualenv
$ pip install -r requirements.txt               # setup pip dependencies
$ chmod +x pretext.sh
```

Run this command to convert AsciiMath markup, written as ``<m>`asciimath goes here</m>`` in `<XML>`, to LaTeX. It also runs `xsltproc` with any arguments specified after `./pretext.sh`.
```shell
$ ./pretext.sh -o <output_dir> <STYLESHEET> <XML>
```
Check [this](http://xmlsoft.org/XSLT/xsltproc.html) for `xsltproc` documentation.

### Example

This command converts AsciiMath markup in files in `samples` folder, stores new XML files to `samples-latex` folder and generates HTML files into `generated-html` folder using `xsltproc`.
```shell
$ ./pretext.sh -o generated-html/ mathbook/xsl/mathbook-html.xsl samples/asciimath.xml
```

#### Notes
- All files in `samples` remain unchanged lest the `pretext.sh` script unexpectedly modify the source XML.
- AsciiMath to LaTeX conversion is done only on files with `.xml`, `.ptx` extensions in `samples`. Other files are copied to `samples-latex` as is.

### Sample AsciiMath XML

To check the AsciiMath to LaTeX conversion on a single XML file, run
```shell
$ python replace.py --xml samples/asciimath.xml
```

## Contact

Please feel free to contact [Yash Mittal](mailto:yashmittal2009@gmail.com) or [create an issue](https://github.com/ymittal/asciimath/issues/new) if you have questions regarding this project.
