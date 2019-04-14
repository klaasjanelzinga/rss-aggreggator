import React, { Component } from 'react';
import './App.css';
import HeaderBar from './HeaderBar';
import Agenda from './Agenda';

class App extends Component {
  render() {
    return (
      <div className="App">
        <HeaderBar />
        <Agenda />
      </div>
    );
  }
}

export default App;
