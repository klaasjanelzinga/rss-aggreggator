import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import GridList from '@material-ui/core/GridList';
import AgendaItem from './AgendaItem'
import { LinearProgress } from '@material-ui/core';

const styles = theme => ({
    agenda: {
        top: '85px',
        left: '0px',
        right: '0px',
        bottom: '0px',
        position: 'absolute',
        justifyContent: 'space-around',
        overflowY: 'hidden',
        marginLeft: '10px',
    },
    gridList: {
        width: '100%',
        height: 450,
        overflow: 'scroll',
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
            events: []
        }
    }

    componentDidMount() {
        fetch('/api/events')
            .then(results => results.json())
            .then(results => {
                this.setState({ events: results, fetched: true })
            })
    }

    render() {
        const {classes} = this.props
        if (this.state.fetched) {
            return (
                <div className={classes.agenda}>
                    <GridList cellHeight={180} cols={1} className={classes.gridList}>
                        {this.state.events.map(event => (
                            <AgendaItem item={event} />
                        ))}
                    </GridList>
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

