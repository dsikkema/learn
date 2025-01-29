"use client"; {/* useState can only be run in client code. next.js components are server
    components bydefault. ut useState can only run in browser for needing to maintain 
  state during session.*/}

import { useState } from 'react';

{/* This is destructuring the props object into its individual variable names 
    And default value!
    */}
export default function Thought({ in_words="I forgot what I was thinking." }) {

  {/* useState returns a tuple of a var (inited with what you gave it) and a callback 
      to update it

      Also, note the ability to destructure into a list as well. Destructuring to/from an
      object relies on the naming of keys, while destructuring to/from a list relies
      on ordering

      the setter callback - it knows that when you give it a non-callable type, then 
      that's just the plain value, whereas when you give it a callable (I guess a one-arg
      callable) that it should use that logic of new = `callable(old)`
      */}
  const [thinkCount, setThinkCount] = useState(1);

  function handleThink() {
    setThinkCount(thinkCount + 1);
  }

  return (
    <div >
      {/* no need to escape single or double quotes in elements */}
      <p>Here's what I was thinking... {in_words}</p>



      {/* 
        - Everytime you click the element, the count goes up
        - onClick is an eventhander -- also not available to server componenets
        */}
      <p onClick={handleThink}>
        (I've thought about this {thinkCount} times so far... click on this sentence
        to make me think about it again!)
      </p>
    </div>
  );
}
