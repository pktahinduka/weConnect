import React, {Component} from 'react';
import { } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';

import HeaderLinks from '../Header/HeaderLinks.jsx';

import imagine from 'assets/img/sidebar-5.jpg';
import logo from 'assets/img/weconnectlogo-2.png';

class Sidebar extends Component{
    constructor(props){
        super(props);
        this.state = {
            width: window.innerWidth
        }
    }
    activeRoute(routeName) {
        return this.props.location.pathname.indexOf(routeName) > -1 ? 'active' : '';
    }
    updateDimensions(){
        this.setState({width:window.innerWidth});
    }
    componentDidMount() {
        this.updateDimensions();
        window.addEventListener("resize", this.updateDimensions.bind(this));
    }
    render(){
        const sidebarBackground = {
            backgroundImage: 'url(' + imagine + ')'
        };
        return (
            <div id="sidebar" className="sidebar" data-color="black" data-image={imagine}>
                <div className="sidebar-background" style={sidebarBackground}></div>
                    <div className="logo">
                            <img src={logo} alt="logo_image"/>
                    </div>
                <div className="sidebar-wrapper">
                    <ul className="nav">
                        { this.state.width <= 991 ? (<HeaderLinks />):null }
                        <li className={this.activeRoute("/user")}>
                            <NavLink to={'/user'} className="nav-link" activeClassName="active">
                                <i className="pe-7s-user"></i>
                                <p>User Profile</p>
                            </NavLink>
                        </li>
                        <li className={this.activeRoute("/Businesses")}>
                            <NavLink to={'/Businesses'} className="nav-link" activeClassName="active">
                                <i className="pe-7s-note2"></i>
                                <p>Businesses</p>
                            </NavLink>
                        </li>
                        <li className={this.activeRoute("/dashboard")}>
                            <NavLink to={'/dashboard'} className="nav-link" activeClassName="active">
                                <i className="pe-7s-graph"></i>
                                <p>Dashboard</p>
                            </NavLink>
                        </li>
                        <li className={this.activeRoute("/notifications")}>
                            <NavLink to={'/notifications'} className="nav-link" activeClassName="active">
                                <i className="pe-7s-bell"></i>
                                <p>Notifications</p>
                            </NavLink>
                        </li>
                    </ul>
                </div>
            </div>
        );
    }
}

export default Sidebar;
