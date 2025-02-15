Requires emcc for wasm compilation: I used `brew install emscripten`

To compile hello.c to wasm:

```
emcc hello.c -o target/hello.js -s EXPORTED_FUNCTIONS='["_square", "_greet"]' -s EXPORTED_RUNTIME_METHODS='["cwrap"]'
```

Note the use of underscores prefixing function names, this reflects how LLVM names things.

Then run a server for the directory:
`python -m http.server`

and visit http://localhost:8000/index.html

When you click greet, the Javascript console in the browser will print Hello, $name.

Shows how to use cwrap to intermediate function calls (perhaps involving strings) and also calling
exported functions directly.
