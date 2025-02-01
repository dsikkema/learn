#/usr/bin/env bash
set -x 
PS4=' $ '

: "cat takes from stdin. no big deal, right?"
echo "hello" | cat

echo aaa > a.txt
echo bbb > b.txt

: "# what do you think is gunna happen now?"
echo "hello" | cat a.txt - b.txt 

: "the hyphen means std. cat conCATenates multiple files but can also concatenate std with other things"

: "that's why cat works with heredocs - the heredoc is meant to go to stdin"
cat << EOF
Multiline 1
Multiline 2
EOF

: "Oh, you're interested in heredocs?"

: "They don't have to be EOF as the delimiter"
cat << ZZZ
something
else
ZZZ

: "They can have variables and cmd substitution"
myvar=7
cat << EOF
My favorite number is $myvar
And I'm in the directory $(pwd)
EOF

: "They can have single and double quotes galore, no problem"
cat << EOF
This is a double quote: "
A single: '
I didn't escape any of this!
EOF

: "Unless you turn that off by quoting the delimiter, single or double"
cat << 'EOF'
My favorite number is $myvar
And I'm in the directory $(pwd)
That's really literal!
EOF

cat << "EOF"
My favorite number is $myvar
And I'm in the directory $(pwd)
Still literal!
EOF

: "Finally, note that < is for input redirection, << is specifically for heredocs!"

: "Ok, encore. There's a third angle operator like that: <<<. It's for putting a single string into stdin."

cat <<< "Just one string!"

