import { Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import React from 'react';

const styles = theme => ({
    title: {
        display: 'none',
        [theme.breakpoints.up('sm')]: {
          display: 'block',
        },
      },
    }
    );


class Title extends React.Component {

    render() {
        const { classes } = this.props;

        return <Typography className={classes.title} variant="h6" color="inherit" noWrap>
                Events from all venues...
            </Typography>


    }
}

Title.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Title);

