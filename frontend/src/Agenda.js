import { Fab, LinearProgress } from '@material-ui/core';
import GridList from '@material-ui/core/GridList';
import { withStyles } from '@material-ui/core/styles';
import { NavigateNext } from '@material-ui/icons';
import PropTypes, { string } from 'prop-types';
import React from 'react';
import AgendaItem from './AgendaItem';

const styles = theme => ({
    agenda: {
        top: '80px',
        left: '0px',
        right: '0px',
        bottom: '0px',
        position: 'absolute',
        justifyContent: 'space-around',
        overflowY: 'scroll',
        overflowX: 'hidden',
        marginLeft: '10px',
    },
    agendaFooter: {
        width: '100%',
        position: 'relative',
        float: 'bottom',
        backgroundColor: '#3f51b5',
        height: '60px',
    },
    nextButton: {
        margin: '20px',
        float: 'right'
    },
    gridList: {
    },
    progressbar: {
        flexGrow: 1,
        marginTop: '10px',
    }
});


class Agenda extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            fetched: false,
            fetch_offset: string,
            events: []
        }
        this.fetchMore = this.fetchMore.bind(this);
        this.endpoint = (window.location.hostname === 'localhost')
            ? 'http://localhost:8080/api/events'
            : '/api/events';
        }

    componentDidMount() {
        console.log('=== fetching items. welcome to the app ===')
        fetch(this.endpoint)
            .then(results => results.json())
            .then(results => {
                this.setState({
                    events: results.events,
                    fetch_offset: results.fetch_offset,
                    fetched: true
                })
            })
    }

    fetchMore() {
        fetch(this.endpoint + '?fetch_offset=' + this.state.fetch_offset)
            .then(results => results.json())
            .then(results => {
                this.setState({
                    events: this.state.events.concat(results.events),
                    fetch_offset: results.fetch_offset,
                    fetched: true
                })
            })

    }

    render() {
        const { classes } = this.props
        if (this.state.fetched) {
            return (
                <div className={classes.agenda}>
                    <GridList cellHeight={180} cols={1} className={classes.gridList}>
                        {this.state.events.map(event => (
                            <AgendaItem item={event} />
                        ))}
                    </GridList>
                    <div className={classes.agendaFooter}>
                        <Fab color="secondary" aria-label="Next" className={classes.nextButton}
                             onClick={this.fetchMore}>
                             <NavigateNext></NavigateNext>
                        </Fab>
                    </div>
                </div>
            );
        } else {
            return (
                <div className={classes.progressbar}>
                    <LinearProgress />
                </div>
            );
        }
    }
}

Agenda.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Agenda);

