import React, { useEffect, useState } from 'react';
import RecordComponent from './components/RecordComponent.tsx';
import logo from './logo.svg';
import './App.css';

function App () {
  // const makeAPICall = async () => {
  //   try {
  //     const response = await fetch('https://localhost:443/cors', {mode:'cors'});
  //     const data = await response.json();
  //     console.log({ data })

  //     if (window.crossOriginIsolated) {
  //       console.log('Cross-origin isolated!');
  //     } else {
  //       console.log('Not cross-origin isolated!');
  //     }
  //   }
  //   catch (e) {
  //     console.log(e)
  //   }
  // }
  // useEffect(() => {
  //   makeAPICall();
  // }, [])

  

  // https://www.stackhawk.com/blog/react-cors-guide-what-it-is-and-how-to-enable-it/

  return (
    <div className="App">
      <header className="App-header">
        <h1>React Cors</h1>
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <RecordComponent />
      </header>

    </div>
  );
};

export default App;
