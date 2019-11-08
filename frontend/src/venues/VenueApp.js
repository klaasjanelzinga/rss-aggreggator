import React, { Component } from 'react';
import HeaderBar from '../headerbar/HeaderBar';
import Venue from './Venue.js'
import { withRouter } from 'react-router-dom';

class VenueApp extends Component {

    constructor() {
        super()
        this.state = {
            venues: [],
            venuesFetched: false
        }
        this.endpoint = '/api/venues';
        this.switchView = this.switchView.bind(this)
    }

    fetchInitialLoad() {
        fetch(this.endpoint)
            .then(results => results.json())
            .then(results => {
                this.setState({
                    venues: results.venues,
                    venuesFetched: true
                })
            })
    }

    componentDidMount() {
        this.fetchInitialLoad()
    }

    render() {
        return (
            <div className="App">
                <HeaderBar />
                <Venue
                    venues={this.state.venues}
                    venuesFetched={this.state.venuesFetched}
                />
            </div>
        );
    }
}

export default withRouter(VenueApp);
