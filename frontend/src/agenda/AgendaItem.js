import { Fab, Typography } from '@material-ui/core';
import GridListTile from '@material-ui/core/GridListTile';
import { withStyles } from '@material-ui/core/styles';
import { OpenInBrowser } from '@material-ui/icons';
import PropTypes from 'prop-types';
import React from 'react';
import { withRouter } from 'react-router-dom';
import ICSButton from './ICSButton';


const styles = theme => ({

    gridListTile: {
        width: '100%',
        marginBottom: '2px',
        height: '195px',
        borderStyle: 'none',
        border: '1px',
        backgroundColor: 'lightgrey',
    },
    tileContents: {
        display: 'flex',
        overflow: 'scroll'
    },
    tileDetails: {
        display: 'block',
        width: '100%',
    },
    tileImage: {
        display: 'block',
        position: 'absolute',
        width: '150px',
        height: '150px',
    },
    agenda_image: {
        width: '150px',
        height: '150px',
    },
    tileItem: {
        position: 'absolute',
        left: '152px',
        textAlign: 'left',
    },
    tileActionBar: {
        display: 'flex',
        position: 'absolute',
        top: '150px',
        width: '100%',
        backgroundColor: 'white',
    },
    grow: {
        flexGrow: '1',
    },
    actionIcon: {
        height: '16px',
        width: '30px',
        margin: '5px',
        backgroundColor: 'lightGrey',
    }
});


class AgendaItem extends React.Component {

    openInBrowser(event, agendaItem) {
        event.preventDefault()
        window.open(agendaItem.url, 'event');
    }

    renderImage(event) {
        const { classes } = this.props;
        if (event.image_url === null) {
            return;
        }
        return <img className={classes.agenda_image} src={event.image_url} alt={event.title} />
    }

    render() {
        const { classes } = this.props;
        const event = this.props.item;
        return (
            <GridListTile className={classes.gridListTile} key={event.id} onClick={() => null}>
                <div className={classes.tileContents} onClick={() => null}>
                    <div className={classes.tileDetails}>
                        <a href={event.url} target='event'>
                            <div className={classes.tileImage}>
                                {this.renderImage(event)}
                            </div>
                            <div className={classes.tileItem}>
                                <Typography variant="h6" color="textPrimary">
                                    {event.title}
                                </Typography>
                                <Typography color="textSecondary" variant="subtitle2">
                                    {event.venue.name} {event.when}
                                </Typography>
                                <Typography variant="subtitle1" color="textSecondary">
                                    {event.description}
                                </Typography>
                            </div>
                        </a>
                    </div>
                    <div className={classes.tileActionBar} >
                        <ICSButton event={event} className={classes.icsButton}></ICSButton>
                            <Fab aria-label="Open in browser" className={classes.actionIcon}
                                onClick={(reactEvent) => this.openInBrowser(reactEvent, event)}>
                                <OpenInBrowser className={classes.calIcon}></OpenInBrowser>
                            </Fab>
                        <div className={classes.grow}></div>
                    </div>
                </div>
            </GridListTile>
        );
    }
}

AgendaItem.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(withRouter(AgendaItem));

