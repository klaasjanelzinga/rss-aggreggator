import { Fab } from "@material-ui/core";
import { withStyles } from '@material-ui/core/styles';
import { CalendarToday } from "@material-ui/icons";
import PropTypes from 'prop-types';
import React from 'react';
import { icsFormatter } from './ics';

const styles = theme => ({
    icalButton: {
        height: '16px',
        width: '30px',
        margin: '5px',
    },
    calIcon: {
        height: '14px',
        width: '20px',
    }
});


class ICSButton extends React.Component {
    constructor(props) {
        super(props);
        this.openICSFile = this.openICSFile.bind(this);
    }

    openICSFile() {
        var cal = icsFormatter();
        cal.addEvent(
            this.props.event.url,
            this.props.event.title,
            this.props.event.description,
            this.props.event.venue.name + ' ' + this.props.event.venue.city,
            this.props.event.when,
            this.props.event.when);
        cal.download(`${this.props.event.title}.ics`)
    }

    render() {
        const { classes } = this.props;

        return <Fab aria-label="Download ical" className={classes.icalButton}
            onClick={this.openICSFile}>
            <CalendarToday className={classes.calIcon}></CalendarToday>
        </Fab>
    }
}

ICSButton.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ICSButton);

