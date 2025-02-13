" use an environment variable to cause this file to be used
" as .vimrc, and first off source the real .vimrc to get all
" its goodies.
"
" e.g. (in .envrc in this same directory, so direnv automatically manages it)
" ```
" export VIMINIT="source .vimrc"
" ```
"
" I suspect this may become useful at some point, where
" I can have custom keymappings / utilities depending
" on my project location
source ~/.vimrc
map <F8> <Esc>:w<CR>:!clear; echo lmao  %<CR>
