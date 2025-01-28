const fs = require('fs');
const _ = require('lodash');

fs.writeFileSync('hello.txt', 'Hello from Node.js\nThis is line 2');
console.log('Wrote file');

fs.readFile('hello.txt', 'utf8', (err, data) => {
  if (err) throw err;
  console.log('File content:', data);
});

const numbers = [1, 2, 3];
console.log('Sum: ', _.sum(numbers));
console.log('Avg: ', _.mean(numbers));

