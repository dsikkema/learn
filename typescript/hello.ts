const world: string = "Earth";
console.log(`Hello, ${world}`);

let arr: number[] = [1, 2];
let arr2: Array<number> = [1, 2];

let my_tuple: [number, string] = [2, "soon"];

let bad: any = "no";

/**
 * Avoid annoying warnings importing the assert package
 */
function assert(v: boolean) {
    if (!v) {
        throw Error("Not true")
    }
}

let inferredStr = "ok";

assert(typeof inferredStr === "string");

// My own types and aliases
type UserID = number;
type User = {
    id: UserID,
    name: string
}

const newUser: User = {
    id: 1,
    name: "Jack"
}

console.log(newUser)