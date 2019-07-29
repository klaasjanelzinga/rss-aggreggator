import { Fab, LinearProgress } from '@material-ui/core';
import GridList from '@material-ui/core/GridList';
import { withStyles } from '@material-ui/core/styles';
import { NavigateNext } from '@material-ui/icons';
import PropTypes from 'prop-types';
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

    render() {
        const { classes } = this.props
        if (this.props.eventsFetched) {
            let moreButton
            let nothingFound
            if (!this.props.isFetchingDone) {
                moreButton = <Fab color="secondary" aria-label="Next" className={classes.nextButton}
                    onClick={this.props.fetchMoreEvents}>
                    <NavigateNext></NavigateNext>
                </Fab>
            }
            if (this.props.events.length === 0){
                nothingFound = <p>Nothing found !</p>
            }

            return (
                <div className={classes.agenda}>
                    {nothingFound}
                    <GridList cellHeight={180} cols={1} className={classes.gridList}>
                        {this.props.events.map(event => (
                            <AgendaItem item={event} key={event.id} />
                        ))}
                    </GridList>
                    <div className={classes.agendaFooter}>
                            {moreButton}
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

