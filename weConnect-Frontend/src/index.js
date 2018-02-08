import React from 'react';
import ReactDOM from 'react-dom';

import {
    BrowserRouter,
    Route,
    Switch
} from 'react-router-dom';

import App from 'containers/App/App.jsx';
import Login from 'views/Login/Login';
import Register from 'views/Register/Register';


import './assets/css/bootstrap.min.css';
import './assets/css/animate.min.css';
import './assets/sass/light-bootstrap-dashboard.css';
import './assets/css/demo.css';
import './assets/css/pe-icon-7-stroke.css';
import './assets/css/login_style.css';


ReactDOM.render((
    <BrowserRouter>
        <Switch>
          if (Login) {<Route path="/login" component={Login}/>} 
          if (Register){<Route path="/register" component={Register}/>} 
          else{<Route path="/" component={App}/>}
        </Switch>
    </BrowserRouter>

),document.getElementById('root'));
