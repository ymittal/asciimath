# Using Node.js

The source in this folder provides an alternative to convert [AsciiMath](http://asciimath.org/) to LaTeX using an existing JavaScript implementation from [asciimathml](https://github.com/asciimath/asciimathml) project.

## Getting started

Start Node server.
```shell
$ cd asciimath/src
$ chmod +x pretext.sh
$ cd server && npm install  # setup node dependencies
$ npm run dev
```

Run this command to convert AsciiMath markup to LaTeX and execute `xsltproc` with any arguments specified after `./pretext.sh`.
```shell
$ ./pretext.sh -o <output_dir> <STYLESHEET> <XML>
```
Check [this](http://xmlsoft.org/XSLT/xsltproc.html) for `xsltproc` documentation.
