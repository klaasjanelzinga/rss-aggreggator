import { Card, CardContent, Typography, withStyles } from '@material-ui/core';
import { withSnackbar } from 'notistack';
import PropTypes from 'prop-types';
import React from 'react';
import GoogleLogin from 'react-google-login';
import { withRouter } from 'react-router-dom';
import UserProfile from './UserProfile';


const styles = {
    card: {
        display: 'flex',
        width: '400px',
        margin: '10px',
    },
    details: {
        display: 'flex',
        flexDirection: 'column',
    },
    content: {
        flex: '2 0 auto',
    },
    disclosure: {
        padding: '10px',
    },
    googleButton: {
        backgroundColor: 'lightgrey',
        padding: '2px',
    }
};

class GoogleCard extends React.Component {

    constructor(props) {
        super(props);

        this.responseGoogle = this.responseGoogle.bind(this);
        this.handleFailure = this.handleFailure.bind(this);
    }

    responseGoogle(response) {
        let userProfile = new UserProfile(
            response.profileObj.givenName,
            response.profileObj.familyName,
            response.profileObj.email,
            response.profileObj.imageUrl,

            response.Zi.access_token,
            response.Zi.id_token,
        );
        this.props.validateSignInWithServer(userProfile);        
    }

    handleFailure(response) {
        this.props.notifyError(`Failed fetching data. ${response}`);
    }

    render() {
        const { classes } = this.props;
        return <Card className={classes.card}>
            <div className={classes.details}>
                <CardContent className={classes.content}>
                    <Typography component="h5" variant="h5">
                        Login using google
                        </Typography>
                    <Typography variant="subtitle1" color="textSecondary">
                        You can sign in to events using your google account.
                        </Typography>
                    <Typography variant="subtitle2" color="textSecondary">
                        Why would you create an account?
                                <ul>
                            <li>Create customized rss feeds (not yet available)</li>
                        </ul>
                    </Typography>
                </CardContent>
                <div className={classes.disclosure}>
                    <Typography variant="subtitle2" >
                        Events for all venues will access the following data in your google profile:
                                <ul>
                            <li>Your email address.</li>
                            <li>Your given name as registered with Google.</li>
                            <li>Your family name as registered with Google.</li>
                        </ul>

                        The data is only used on this site and will not be shared. By clicking on the login
                        button you acknowledge this.
                        </Typography>

                </div>
                <div className={classes.googleButton}>
                    <GoogleLogin
                        clientId="533901621191-qeb3c8r94s21h1q3vld1jmapc6blkp9s.apps.googleusercontent.com"
                        buttonText="Login"
                        onSuccess={this.responseGoogle}
                        onFailure={this.handleFailure}
                        className={classes.googleButton}
                        cookiePolicy={'single_host_origin'}
                    />
                </div>
            </div>
        </Card>
    }
}

GoogleCard.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(withRouter(withSnackbar(GoogleCard)));

