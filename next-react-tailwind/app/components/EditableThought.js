"use client";

import { useState } from 'react';

export default function EditableThought() {

  {/*
    - don't have to define this as a class, the object functions like a dictionary
  */}
  const [thought, setThought] = useState({
    inWords: "Knowing how to be a good human will always matter",
    epistemicStatus: true
  })

  const [newThoughtInput, setNewThoughtInput] = useState("");


  {/* 
    - the event handler for changing a value in the input field. Invoked
    even when just one character is changed, every time, to update the 
    var.
    - setting input val to "" will cause the input field to revert back
    to its placeholder value. We're setting value={input} in the input
    field's html, so when that's an empty string, the placeholder takes
    over
  */}
  function handleNewThoughtInputChange(event){
    setNewThoughtInput(event.target.value);
  }

  {/*
    * - spread operator blows up obj into key-val pairs
    * - pairs will be overridden by later, explicitly passed in vals
    * - We could, if we wanted, use multiple object spreads with the latter
    *   overriding the former.
    * - And you can also use the spread syntax in a
    *   function signature to collect variable number
    *   of args as a list.
  */}
  function handleUpdateWords() {
    setThought(
      prevThought => ({
        ...prevThought,
        inWords: newThoughtInput
      })
    );

    setNewThoughtInput("");
  }

  function handleUpdateStatus() {
    setThought(
      prevThought => ({
        ...prevThought,
        epistemicStatus: !prevThought.epistemicStatus
      })
    );
  }


  {/*
    - styling:
      - ml-2 means margin left (padding) to separate elements
      - border, rounded self-explanatory
      - text-black: for some reason default's to grey in this app? Set to black for visibility
      - w-96: a preset width option
  */}
  return (
    <div>
      <p>Another thought: {thought.inWords}</p>
      <p>Epistemic status: {thought.epistemicStatus ? 'Verily' : 'Inconceivable'}</p>
      <input 
        className="border rounded text-black w-96"
        type="text"
        value={newThoughtInput}
        onChange={handleNewThoughtInputChange}
        placeholder="Enter a different thought here"
      />
      <button className="ml-2 border rounded" onClick={handleUpdateWords}>Update the other Thought</button>
      <button className="ml-2 border rounded" onClick={handleUpdateStatus}>Toggle the other Thought's status</button>
    </div>
  );
}
