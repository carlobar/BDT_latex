## BDT_latex

BDT_latex.py is a program that automates the _Belcher Diagnostic Test_ for _LaTeX_ documents. The _Belcher Diagnostic Test_ was invented to improve academic writing by Wendy Laura Belcher in her book [_Writing Your Journal Article in Twelve Weeks: A Guide to Academic Publishing Success_ ](http://wendybelcher.com/writing-advice/writing-your-journal-article-in-twelve) and is copyrighted by her. The program is designed to implement the test on projects that use multiple files, such as _TeX_ files or images. Instructions on using the test to improve writing are in Belcher’s book.


## Usage

`python BDT_latex.py examples.tex`

The script creates new TeX files with suffix `_BDT`  (e.g.,  `examples_BDT.tex`) in the same directory of the original file. The new files can be compiled with LaTeX to proceed with the Belched Diagnostic Test.


## Documentation

The full documentation of the code is available at [here](https://github.com/carlobar/BDT_latex/blob/master/documentation).


## Requirements

The code can be executed with Python 2.7 or later. The program requires the LaTeX package `xcolor`.


## How to Contribute

Contributions are welcome. To make modifications fork the repository and clone it in your computer to make changes with 

`$ git clone {Repository_URL}`

Once you have pushed changes to your local directory, you can make a pull request from GitHub.

Please do not publish any explanation of the Belcher Diagnostic Test without Belcher's permission because 1) the book gives a detailed explanation of the method; and 2) that might lead to a copyright infringement.


## License

The contents of this repository are covered under the [MIT License](https://github.com/carlobar/BDT_latex/blob/master/LICENSE).



