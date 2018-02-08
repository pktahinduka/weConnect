import React, { Component } from 'react';
import axios from 'axios';

class Login extends Component{

  constructor() {
    super();
    this.state = {
      username: '',
      email: '',
      password: '',
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
  componentDidMount() {
    this.getUsers();
  };
  getUsers() {
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
    .then((res) => { this.setState({ users: res.data.data.users }); })
    .catch((err) => {  });
  };
  addUser(event) {
    event.preventDefault();
    const data = {
      username: this.state.username,
      email: this.state.email,
      password: this.state.password
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
    let data = {
      username: this.state.username,
      email: this.state.formData.email,
      password: this.state.formData.password,
    };
    const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/register`
    axios.post(url, data)
    .then((res) => {
      this.setState({
        formData: {username: '', email: '', password: '' },
        username: '',
        email: '',
        password: '',
        isAuthenticated: true,
      });
      window.localStorage.setItem('authToken', res.data.auth_token);
      this.props.history.push('/login');
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
                             name="username"
                             className="login__input name" 
                             placeholder="Username"
                             value={this.state.formData.username}
                             onChange={this.handleFormChange}
                             />
                          </div>
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
                          value="Submit">Register
                          </button>
                          </div>
                         </form>
                      </div>
                    </div>
               </div> );
	        }
        }

export default Login;