import React, { Component } from 'react';
import { Grid, Row,
        FormGroup, FormControl, ControlLabel, Col} from 'react-bootstrap';
import {Card} from 'components/Card/Card.jsx';
import {FormInputs} from 'components/FormInputs/FormInputs.jsx';
    
import Button from 'elements/CustomButton/CustomButton.jsx';
import axios from 'axios';
import NotificationSystem from 'react-notification-system';
import {style} from "variables/Variables.jsx";


class AddItems extends Component {

  constructor() {
    super();
    this.state = {
      business_name: '',
      business_category: '',
      business_addr: '',
      business_desc:'',
      created_by:'',
      formData: {
         business_name: '',
         business_category: '',
         business_addr: '',
         business_desc:'',
         created_by:''
      },
      _notificationSystem: null
    };
    this.handleClick = this.handleClick.bind(this);
    this.componentDidMount = this.componentDidMount.bind(this);
    this.addBusiness = this.addBusiness.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleBusinessFormSubmit = this.handleBusinessFormSubmit.bind(this);
    this.handleFormChange= this.handleFormChange.bind(this);

  };
  componentDidMount(){
      this.setState({_notificationSystem: this.refs.notificationSystem})
  }

  handleClick(position){
    var level = 'error'; // 'success', 'warning', 'error' or 'info'
    if(this.state.business_name === '' || 
       this.state.business_category === '' ||
       this.state.business_addr === ''){
    this.state._notificationSystem.addNotification({
        title: (<span data-notify="icon" className="pe-7s-info"></span>),
        message: (
            <div>
                Please check that you filled in all the details before <b>Submit</b>.
            </div>
        ),
        level: level,
        position: position,
        autoDismiss: 5,
    });
    }
  }

  addBusiness(event) {
    event.preventDefault();
    const data = {
      business_name: this.state.business_name,
      business_category: this.state.business_category,
      business_addr: this.state.business_addr,
      business_desc: this.state.business_desc,
      created_by: this.state.created_by,
    };
    axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/businesses`, data)
    .then((res) => {
      this.getBusinesses();
    })
    .catch((err) => { console.log(err); });
  }

  handleChange(event) {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  };
  handleBusinessFormSubmit(event) {
    event.preventDefault();
    const user_name = window.localStorage.username;
    let data = {
      business_name: this.state.business_name,
      business_category: this.state.business_category,
      business_addr: this.state.business_addr,
      business_desc: this.state.business_desc,
      created_by: user_name,
    };

    const jwtStr = window.localStorage.getItem('authToken');
    const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/businesses`
    axios.post(url, data,
         {
            'headers': {
            'Authorization': 'Bearer ' + jwtStr
            }
         })
    .then((res) => {
      this.setState({
        formData: {business_name: '', business_category: '', business_addr: '', business_desc: '' },
        business_name: '',
        business_category: '',
        business_addr: '',
        business_desc:''
      });
      window.localStorage.setItem('message', res.data.message);
      this.props.history.push('/Businesses')
    })
    .catch((err) => { console.log(err); });

  };
  handleFormChange(event) {
    const obj = this.state.formData;
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  };

    render() {

        return (
            <div className="content">
                <Grid fluid>
                    <Row>
                        <Col md={12}>
                            <Card
                                title="Add A Business"
                                content={
                                    <form onSubmit={(event) => this.handleBusinessFormSubmit(event)}>

                                        <FormInputs 
                                            ncols = {["col-md-6", "col-md-6"]}

                                            proprieties = {[
                                                {
                                                 label : "Business name",
                                                 type : "text",
                                                 name : "business_name",
                                                 bsClass : "form-control",
                                                 placeholder : "Business name",
                                                 defaultValue : "Drarter Homes",
                                                 value: this.state.formData.business_name,
                                                 onChange: this.handleFormChange
                                                },
                                                {
                                                    label : "Business Address",
                                                    type : "text",
                                                    name : "business_addr",
                                                    bsClass : "form-control",
                                                    placeholder : "Home Adress",
                                                    defaultValue : "Garden City Mall",
                                                    value: this.state.formData.business_addr,
                                                    onChange: this.handleFormChange
                                                }
                                            ]}
                                        />                                          

                                        <FormInputs 
                                            ncols = {["col-md-12"]}

                                            proprieties = {[
                                                {
                                                 label : "Business Category",
                                                 type : "text",
                                                 name : "business_category",
                                                 bsClass : "form-control",
                                                 placeholder : "Business Category",
                                                 defaultValue : "Drarter Homes",
                                                 value: this.state.formData.business_category,
                                                 onChange: this.handleFormChange
                                                }
                                            ]}
                                        /> 

                                        <Row>
                                            <Col md={12}>
                                                <FormGroup controlId="formControlsTextarea">
                                                    <ControlLabel>About The Business</ControlLabel>
                                                    <FormControl 
                                                    rows="5" 
                                                    componentClass="textarea" 
                                                    bsClass="form-control"
                                                    name="business_desc" 
                                                    placeholder="Here can be your description" 
                                                    defaultValue="Dealers in smart home technology."
                                                    value={this.state.formData.business_desc}
                                                    onChange={this.handleFormChange}                                            
                                                    />
                                                </FormGroup>
                                            </Col>
                                        </Row>
                                        <NotificationSystem ref="notificationSystem" style={style}/>
                                        <Button
                                            bsStyle="info"
                                            pullRight
                                            fill
                                            onClick={this.handleClick.bind(this,'tc')}
                                            type="submit"
                                        >
                                           Submit Business
                                        </Button>
                                        
                                        <div className="clearfix"></div>
                                    </form>
                                }
                            />
                        </Col>

                    </Row>
                </Grid>
                
            </div>
            
        );
    }
}

export default AddItems;
