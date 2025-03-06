type UserID = number;
type User = {
    id: UserID,
    name: string
}

const newUser: User = {
    id: "not a number",
    name: "Jack"
}

console.log(newUser)