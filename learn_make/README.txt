TODO:
 - make both example Makefiles use proper dependency so unnecessary recompliations don't happen
 - will be able to use this as a template for Makefiles in c/ directory

in top dir, the Makefile compiles and runs any c program "myfile.c" with "make myfile"

in bottom dir, no matter what make rule you give it, "make lol" or "make abc" etc, it will
compile and run the whole project

It's silly because I'm basically treating the Makefile as a one liner shell script. I'm not
doing anything the way Make is actually supposed to be used (yet). 

I imagine this being useful for fast coding in C projects where in some directory I might want
a shortcut to just run the single file, in other projects I might want that same shortcut
to run the whole project (let's say, run the test suite, even if I'm in one of the data structure
files that is used in the test suite which I'm trying to debug and fix). Then, whether I'm using
VIM or VS Code, I can just have one single shortcut bind to "make $filename" (etc) which will,
according to where the file is located, either just compile/run that file, or the whole
project.

