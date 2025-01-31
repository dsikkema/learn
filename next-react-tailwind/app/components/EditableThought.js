"use client";

import { useEffect, useState, useRef } from 'react';


export default function EditableThought() {

  var defaultThought = {
    inWords: "Knowing how to be a good human will always matter",
    epistemicStatus: true
  }

  /**
   * For my most sophisticated web development trick yet, I'm going to use "loading" state
   * to prevent showing anything until "loading" is complete: that is, until client-side
   * loading is complete.
   * 
   * Without this state, I have a FOUC problem: "flash of unstyled content". It's because
   * server doesn't have access to local storage and hence flashes the default thought \
   * value into the html, and then, a fraction of a second later, the client-side effect
   * overwrites this with the saved thought taken from localStorage.
   * 
   * So instead: loading = true, until the client turns it off. And the component will
   * render nothing until loading = false.
   * 
   * The clientside process of taking the html that the server has sent over and attaching
   * event handlers, creating components, setting up hooks (like useEffect), etc, that's
   * called hydration.
   * 
   */
  const [loading, setLoading] = useState(true);

  /**
   * A note here about the dependency array, the second arg to useEffect.
   * 
   * if nothing provided: (client) runs this _every render_.
   * 
   * if [] provided: client runs this _only on mount (aka first client render)_.
   * 
   * if [a, b, c] provided, react will compare the passed-in values
   * of those elements to their previous values, and only run if one
   * of them changed.
   * 
   * This will become relevant again later below, to stop infinite loops.
   */
  useEffect(() => {
    setLoading(false);
  }, []);

  {/*
    - don't have to define this "Thought" object as a class, the object functions like a dictionary
    - another note: part of the essential way state works is that when the state
      setter is called (a function which, remember, is actually created by the 
      react internals), a re-render is schedule. You don't want a re-render? Then
      don't set state. Simple as.
    - To add onto that point, there's a reason why, when I call the setter, and then
      a re-render is triggered, and this same code is called again, there's a reason
      why the default won't clobber over the value I just set. It's actually saved. 
      You (like I did) may wonder, how does react magically know what the value of the
      state is, when I'm not passing any kind of key or ID into useState for it to use
      to retrieve the current value? Well, it's magic, basically. Don't ask prying
      questions about the nature of magic. Just kidding. The ordering is critical. So
      you can't (shouldn't, really... this is javascript you can do whatever you want)
      put useState invocations inside loops or if statements or in places where the 
      number and ordering of its calls is variable or non-static. It uses the order 
      of call to index into a list of states, in the internal magic.
    - Can pass an initial value into useState, or a callable that will produce the
      initial value. In other places I just pass the value, here I'll pass a callable
      which produces the same thing, only to show the syntax.
  */}
  const [thought, setThought] = useState(() => {
    return defaultThought;
  })

  /**
   * Note the necessity of [] dep array here. If this ran on every
   * render, or if it ran whenever thought was updated, there would
   * be an infinite loop. Even if I passed [thought], and the string
   * values were the same, the Object.is() comparison would be false
   * because the object references of the string are different.
   * 
   * So [] makes it only run once (which is really all I need because
   * I'm just doing initialization) and cuts off infinite loop.
   */
  useEffect(() => {
    var saved = localStorage.getItem('saved-thought');
    if (saved) {
      setThought(JSON.parse(saved));
    }
  }, [])

  /**
   * Note why [thought] does _not_ cause infinite loop here. This effect
   * does not call setThought, or set any state at all, and doesn't inherently
   * trigger a re-render.
   * 
   * And we specifically need to run it, if and only if thought changed,
   * because how else would we set the value in local storage? And why
   * would we need to set it if it hasn't changed from its previous value?
   */
  useEffect(() => {
    // save thought to local storage
    var toSave = JSON.stringify(thought);
    if (toSave) {
      localStorage.setItem('saved-thought', toSave);
    }
  }, [thought])
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
  function handleNewThoughtInputChange(event) {
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

  const inputRef = useRef(null);

  /**
   * Autofocus on the input on page load; this "inputRef" is used in the input element.
   */
  useEffect(() => {
    /**
     * optional chaining operator. x=null; x?.func(); won't blow up, it just won't call func()
     * 
     * This is needed here specifically because of our "loading" check! serverside render won't return
     * the component, just null, and won't do the "inputRef" magic stuff. Only the client side will.
     * So need to guard against a null inputRef.
     * 
     * Why [loading]? Because, on mounting, inputRef won't be set yet, and hence the input won't
     * receive focus. However, the effect will still be run, with the state loading=true (even
     * though the mount calls setLoading(false), that's asynchronous! It will take effect only
     * on re-render, see logs in this effect for proof). Then the second render will happen
     * with loading = false, which will register as a change. From that point forth, until the 
     * page is refreshed or accesses again, loading will never again change state and this effect
     * won't be run again.
     * 
     * Browser logs:
     * Executing focus effect: loading=true  
     * Executing focus effect: loading=false 
     * 
     * Note also the batching of state updates: if I call setSomething and setSomethingElse, those two
     * things will _schedule_ re-renders that may be batched together, rather than necessarily two 
     * different re-renders happening.
     */
    console.log(`Executing focus effect: loading=${loading}`);
    inputRef.current?.focus(); 
  }, [loading]);

  {/*
    - styling:
      - ml-2 means margin left (padding) to separate elements
      - border, rounded self-explanatory
      - text-black: for some reason default's to grey in this app? Set to black for visibility
      - w-96: a preset width option
  */}
  return loading ? null : (
    <div>
      <p>Another thought: {thought.inWords}</p>
      <p>Epistemic status: {thought.epistemicStatus ? 'Verily' : 'Inconceivable'}</p>
      {/**
         - htmlFor attr connects the label to the input's id for a11y
       */}
      <label
        className='label w-96'
        htmlFor='thought-input'
      >Thinking anything new?: (Press z to submit, lol)</label>
      {/**
          - Note about onKeyDown callable:
            - Ok, more javascript magic. First, using short-circuiting here for conditional logic.
              IFF key is z, then execute the next functions.
            - But then the comma operator comes next. syntax is (f(), g()), and g() is returned value.
              But doesn't need to be in parens.
              It is built into javascript, and allows for multiple functions that ostensibly perform
              useful side-effects to run prior to the last one which will be the return value.
            - In our case, all of the functions in the comma-operator express are "just" side-effects
              and return value is unused. Namely, the side effects are that 'z' will submit the update
              but also prevent the default event-handling behavior of the key-down, and not let 'z'
              get typed into the input.
          - More comments about comments: I cannot put this comment between attributes. The multiline
            comments may only be between elements. And no, single line comments don't work anywhere 
            between or in elements.
          - These elements are called "JSX elements" or just "elements", by the way.
          - inputRef: connects this element directly to the dom element, so that (above) we can use
            an affect that will autofocus this element on page load.
          */}
      <input
        className="ml-2 border rounded text-black w-96"
        id='thought-input'
        ref={inputRef}
        type="text"
        value={newThoughtInput}
        onChange={handleNewThoughtInputChange}
        placeholder="Enter a different thought here"
        onKeyDown={e => e.key === 'z' && (handleUpdateWords(), e.preventDefault())}
      />
      <button className="ml-2 border rounded" onClick={handleUpdateWords}>Update the other Thought</button>
      <button className="ml-2 border rounded" onClick={handleUpdateStatus}>Toggle the other Thought's status</button>
    </div>
  );
}
