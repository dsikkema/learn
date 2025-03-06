To run with typechecking, have to run the compiler (tsc) _then_ the tsx interpretter separately.

I made a `bin/` dir (added onto my path with `direnv`) containing symlinks into `node_modules/.bin` specifically for tsc and tsx,
and also made a 'compile then run' utility there called runtypescript.

```bash
 $ runtypescript hello.ts
Hello, Earth
{ id: 1, name: 'Jack' }


 $ runtypescript type_error.ts 
type_error.ts:8:5 - error TS2322: Type 'string' is not assignable to type 'number'.

8     id: "not a number",
      ~~

  type_error.ts:3:5
    3     id: UserID,
          ~~
    The expected type comes from property 'id' which is declared here on type 'User'


Found 1 error in type_error.ts:8
```

It's necessary to install a separate runner (tsx) to directly interpret TS on the command-line, the typescript package includes the TS-to-JS
compiler but not an interpretter.
