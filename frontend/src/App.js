import React, { Component } from 'react';
import Agenda from './agenda/Agenda';
import './App.css';
import HeaderBar from './headerbar/HeaderBar';

class App extends Component {

  constructor() {
    super()
    this.state = {
      searchText: '',
      eventsFetched: false,
      fetch_offset: '',
      events: [],
      is_searching: false,
      is_fetching_done: false,
      currentView: "TODAY",
    }
    this.endpoint = '/api';
    this.eventEndpoint = `${this.endpoint}/events`
    this.todayEventEndpoint = `${this.endpoint}/events/today`
    this.tomorrowEventEndpoint = `${this.endpoint}/events/tomorrow`
    this.searchEndpoint = `${this.endpoint}/search`

    this.searchEvents = this.searchEvents.bind(this);
    this.switchView = this.switchView.bind(this);
  }

  is_fetching_done(base64EncodedDone) {
    var base64 = require('base-64');
    var decoded = base64.decode(base64EncodedDone)
    return decoded === 'DONE'
  }

  fetchMoreEvents() {
    this.setState({ 'eventsFetched': false })
    if (this.state.is_searching) {
      this.concatFetchedEvents(`${this.searchEndpoint}?fetch_offset=${this.state.fetch_offset}&term=${this.state.searchText}`)
    } else {
      this.concatFetchedEvents(`${this.eventEndpoint}?fetch_offset=${this.state.fetch_offset}`)
    }
  }

  concatFetchedEvents(endpoint) {
    fetch(endpoint)
      .then(results => results.json())
      .then(results => {

        this.setState({
          events: results.events,
          fetch_offset: results.fetch_offset,
          eventsFetched: true,
          is_fetching_done: this.is_fetching_done(results.fetch_offset),
        })
      })
  }

  searchEvents(searchTerms) {
    if (searchTerms === '') {
      this.fetchTodayEvents()
      return;
    }
    this.setState({
      searchText: searchTerms,
      eventsFetched: false,
      fetch_offset: '',
      events: [],
      is_searching: true,
      currentView: "SEARCH_RESULTS",
    })
    this.fetchEvents(`${this.searchEndpoint}?term=${searchTerms}`)
  }

  fetchEvents(endpoint) {
    fetch(endpoint)
      .then(results => results.json())
      .then(results => {
        this.setState({
          events: results.events,
          fetch_offset: results.fetch_offset,
          eventsFetched: true,
          is_fetching_done: this.is_fetching_done(results.fetch_offset),
        })
      })
  }

  fetchTodayEvents() {
    this.fetchEvents(this.todayEventEndpoint);
  }

  fetchTomorrowEvents() {
    this.fetchEvents(this.tomorrowEventEndpoint);
  }

  fetchAllEvents() {
    this.fetchEvents(this.eventEndpoint);
  }

  componentDidMount() {
    this.fetchTodayEvents();
  }

  switchView(newView) {
    console.log('swiching to ', newView)
    this.setState({ currentView: newView })
    if (newView === "ALL" || newView === "SEARCH_RESULTS") {
      this.fetchAllEvents();
      this.setState({ searching: false, searchTerms: '' });
    }
    if (newView === "TOMORROW") {
      this.fetchTomorrowEvents();
      this.setState({ searching: false, searchTerms: '' });
    }
    if (newView === "TODAY") {
      this.fetchTodayEvents();
      this.setState({ searching: false, searchTerms: '' });
    }
  }

  render() {
    return (
      <div className="App">
        <HeaderBar
          selected={this.state.currentView}
          switchView={(newView) => this.switchView(newView)}
          searchEvents={(searchTerms) => this.searchEvents(searchTerms)}
        />

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
