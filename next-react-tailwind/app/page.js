import Greeting from './components/Greeting';

export default function Home() {
  return (
    <div >
      {/* If I omit the text-xl, tailwind will make the element the same size as h2, p, etc.
      It equalizes element sizes so they must be explicitly set.
        */}
      <h1 className="text-xl">Learning React</h1>
      <Greeting name="All Living Things" />  {/* must be capital; react uses this convention to know
                      that it must call React.createElement(Greeting, null) */}
    </div>
  );
}
