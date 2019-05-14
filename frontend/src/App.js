import React, { Component } from 'react';
import Agenda from './Agenda';
import './App.css';
import HeaderBar from './HeaderBar';

class App extends Component {

  constructor() {
    super()
    this.state = {
      searchText: '',
      searchResults: [],
      eventsFetched: false,
      fetch_offset: '',
      events: [],
      is_searching: false,
      is_fetching_done: false,
    }
    this.endpoint = (window.location.hostname === 'localhost')
      ? 'http://localhost:8080/api'
      : '/api';
    this.eventEndpoint = `${this.endpoint}/events`
    this.searchEndpoint = `${this.endpoint}/search`
  }
  
  is_fetching_done(base64EncodedDone) {
    var base64 = require('base-64');
    var decoded = base64.decode(base64EncodedDone)
    return decoded === 'DONE'
  }

  fetchMoreEvents() {
    this.setState({ 'eventsFetched': false })
    if (this.state.is_searching) {
      this.fetchMoreSearchEvents()
    } else {
      this.fetchMoreRegularEvents()
    }
  }

  fetchMoreRegularEvents() {
    fetch(this.eventEndpoint + '?fetch_offset=' + this.state.fetch_offset)
      .then(results => results.json())
      .then(results => {
        
        this.setState({
          events: this.state.events.concat(results.events),
          fetch_offset: results.fetch_offset,
          eventsFetched: true,
          is_fetching_done: this.is_fetching_done(results.fetch_offset),
        })
      })
  }


  fetchMoreSearchEvents() {
    fetch(`${this.searchEndpoint}?fetch_offset=${this.state.fetch_offset}&term=${this.state.searchText}`)
      .then(results => results.json())
      .then(results => {
        this.setState({
          events: this.state.events.concat(results.events),
          fetch_offset: results.fetch_offset,
          eventsFetched: true,
          is_fetching_done: this.is_fetching_done(results.fetch_offset),
        })
      })
  }

  searchEvents(searchTerms) {
    if (searchTerms === '') {
      this.fetchInitialLoad()
      return;
    }
    this.setState({
      searchText: searchTerms,
      searchResults: [],
      eventsFetched: false,
      fetch_offset: '',
      events: [],
      is_searching: true,
    })
    fetch(`${this.searchEndpoint}?term=${searchTerms}`)
      .then(results => results.json())
      .then(results => {
        this.setState({
          events: this.state.events.concat(results.events),
          fetch_offset: results.fetch_offset,
          eventsFetched: true,
          is_fetching_done: this.is_fetching_done(results.fetch_offset),
        })
      })
  }

  fetchInitialLoad() {
    fetch(this.eventEndpoint)
      .then(results => results.json())
      .then(results => {
        this.setState({
          events: results.events,
          fetch_offset: results.fetch_offset,
          eventsFetched: true,
          is_searching: false,
          is_fetching_done: this.is_fetching_done(results.fetch_offset),
        })
      })
  }

  componentDidMount() {
    console.log('=== welcome to the app ===')
    this.fetchInitialLoad()
  }


  render() {
    return (
      <div className="App">
        <HeaderBar searchEvents={(searchTerms) => this.searchEvents(searchTerms)} />
        <Agenda
          events={this.state.events}
          eventsFetched={this.state.eventsFetched}
          isFetchingDone={this.state.is_fetching_done}
          fetchMoreEvents={() => this.fetchMoreEvents()}
        />
      </div>
    );
  }
}

export default App;
