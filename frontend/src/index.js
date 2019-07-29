import { SnackbarProvider } from 'notistack';
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route } from "react-router-dom";
import App from './App';
import './index.css';
import * as serviceWorker from './serviceWorker';
import profile from './signin/profile';
import signin from './signin/signin';
import signout from './signin/signout';



ReactDOM.render(
    <Router>
        <SnackbarProvider 
                maxSnack={3} 
                autoHideDuration={2000}
                anchorOrigin={{ vertical: 'top', horizontal: 'right', }}>
            <Route exact path="/" component={App} />
            <Route exact path="/user/signin" component={signin} />
            <Route exact path="/user/signout" component={signout} />
            <Route exact path="/user/profile" component={profile} />
        </SnackbarProvider>
    </Router>
    ,
    document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
