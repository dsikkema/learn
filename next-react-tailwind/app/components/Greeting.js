import Thought from './Thought'
export default function Greeting(props) {
  return (
    <div >
      {/* using props like this is called expression interpolation */}
      <h2>Hello, {props.name}!</h2> {/* html-like attrs are given into a javascript object called props */}
      <Thought in_words="you can't spell artificial without art"/>
    </div>
  );
}
