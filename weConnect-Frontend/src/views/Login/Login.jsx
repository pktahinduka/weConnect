import React, { Component } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

class Register extends Component{

  constructor() {
    super();
    this.state = {
      users: [],
      username: '',
      email: '',
      formData: {
        username: '',
        email: '',
        password: ''
      },
      isAuthenticated: false,
    };
    this.addUser = this.addUser.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
    this.handleFormChange= this.handleFormChange.bind(this);
  };

  addUser(event) {
    event.preventDefault();
    const data = {
      username: this.state.username,
      email: this.state.email
    };
    axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, data)
    .then((res) => {
      this.getUsers();
      this.setState({ username: '', email: '' });
    })
    .catch((err) => { console.log(err); });
  }
  handleChange(event) {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  };
  handleUserFormSubmit(event) {
    event.preventDefault();
    const formType = window.location.href.split('/').reverse()[0];
    let data = {
      email: this.state.formData.email,
      password: this.state.formData.password,
    };
    if (formType === 'register') {
      data.username = this.state.formData.username;
    }
    const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${formType}`
    axios.post(url, data)
    .then((res) => {
      this.setState({
        formData: {username: '', email: '', password: '' },
        username: '',
        email: '',
        isAuthenticated: true,
      });
      window.localStorage.setItem('authToken', res.data.auth_token);
      window.localStorage.setItem('username', res.data.username);
      this.props.history.push('/user');
    })
    .catch((err) => { console.log(err); });

  };

  handleFormChange(event) {
    const obj = this.state.formData;
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  };

	render(){

		return(
                <div className="cont">   
                  <div className="demo">
                    <div className="login">
                      <div className="logo_sec"></div>
                        <form onSubmit={(event) => this.handleUserFormSubmit(event)}>
                         <div className="login__form">
                           <div className="login__row">
                             <svg className="login__icon name svg-icon" viewBox="0 0 20 26">
                               <path d="M0,20 a10,8 0 0,1 20,0z M10,0 a4,4 0 0,1 0,8 a4,4 0 0,1 0,-8" />
                             </svg>
                             <input 
                             type="text" 
                             name="email"
                             className="login__input name" 
                             placeholder="Email"
                             value={this.state.formData.email}
                             onChange={this.handleFormChange}
                             />
                          </div>
                           <div className="login__row">
                             <svg className="login__icon pass svg-icon" viewBox="0 0 20 26">
                               <path d="M0,20 20,20 20,8 0,8z M10,13 10,16z M4,8 a6,8 0 0,1 12,0" />
                             </svg>
                             <input 
                             type="password"
                             name="password" 
                             className="login__input pass" 
                             placeholder="Password"
                             value={this.state.formData.password}
                             onChange={this.handleFormChange}/>
                          </div>
                          <button 
                          type="submit" 
                          className="login__submit"
                          value="Submit">Sign in</button>
                          <p className="login__signup">Don't have an account? &nbsp;<Link to={'/register'}><a>Sign up</a></Link></p>
                         </div>
                         </form>
                      </div>
                    </div>
               </div> );
	        }
        }

export default Register;