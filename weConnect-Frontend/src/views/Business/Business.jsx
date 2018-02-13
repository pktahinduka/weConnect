import {BusinessCard} from 'components/BusinessCard/BusinessCard.jsx';
import React, { Component } from 'react';
import { FormGroup, FormControl, ControlLabel } from 'react-bootstrap';
import {Card} from 'components/Card/Card.jsx';
import avatar from "assets/img/faces/face-9.png";
import bgImage from "assets/img/businessprof.jpg";
import Button from 'elements/CustomButton/CustomButton.jsx';
import axios from 'axios';

import { Grid, Col } from 'react-bootstrap';

class Business extends Component {

  constructor(){
    super();
    //const business = this.state.businesses.find(p => p.id === );
    //const business_name = Object(business).business_name;
    this.state = {
      businesses:[],
      reviews: [],
      business_name: '',
      review_text: '',
      created_by:'',
      formData: {
         business_name: '',
         review_text: '',
         created_by:''
      },
    };
    this.componentDidMount = this.componentDidMount.bind(this);
    this.addReview = this.addReview.bind(this);
    this.handleReviewFormSubmit = this.handleReviewFormSubmit.bind(this);
    this.handleFormChange= this.handleFormChange.bind(this);
  };

  componentDidMount() {
    this.getBusinesses();
    this.getReviews();
  };

  getBusinesses() {
    const jwtStr = window.localStorage.getItem('authToken');
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/businesses`,
         {
            'headers': {
            'Authorization': 'Bearer ' + jwtStr
            }
         })
    .then((res) => { this.setState({ businesses: res.data.data.businesses });
        })
    .catch((err) => {  });
  };

  getReviews() {
    const jwtStr = window.localStorage.getItem('authToken');
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/reviews`,
         {
            'headers': {
            'Authorization': 'Bearer ' + jwtStr
            }
         })
    .then((res) => { 
      this.setState({ reviews: res.data.data.reviews }); 
      })
    .catch((err) => {  });
  };

  addReview(event) {
    event.preventDefault();
    const jwtStr = window.localStorage.getItem('authToken');
    const data = {
      business_name: this.state.business_name,
      review_text: this.state.review_text,
      created_by: this.state.created_by,
    };
    axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/reviews`, data,
         {
            'headers': {
            'Authorization': 'Bearer ' + jwtStr
            }
         })
    .then((res) => {
      this.getReviews();
    })
    .catch((err) => { console.log(err); });
  }
  
  handleReviewFormSubmit(event) {
    event.preventDefault();
    
    const jwtStr = window.localStorage.getItem('authToken');
    const user_name = window.localStorage.username;
    const business_name = window.localStorage.business;

    let data = {
      business_name: business_name,
      review_text: this.state.review_text,
      created_by: user_name,
    };
    const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/reviews`
    axios.post(url, data,
         {
            'headers': {
            'Authorization': 'Bearer ' + jwtStr
            }
         })
    .then((res) => {
      this.setState({
        formData: {business_name: '', review_text: '' },
        business_name: '',
        review_text: ''
      });
      window.localStorage.setItem('message', res.data.message);
    })
    .catch((err) => { console.log(err); });

  };
  handleFormChange(event) {
    const obj = this.state.formData;
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  };
    render() {

        const business = this.state.businesses.find(p => p.id === Number(this.props.location.pathname.slice(10)));
        const business_name = Object(business).business_name;
        const business_category = Object(business).business_category;
        const created_by = Object(business).created_by;

        window.localStorage.setItem('business', business_name);


        return (
            <div className="content">
                <Grid fluid>
                    
                        <Col md={12}>
                            <BusinessCard
                                bgImage={bgImage}
                                avatar={avatar} // eslint-disable-next-line
                                role={business_name}
                                name={"@"+created_by}
                                userName="Created by"
                                category="Category"
                                bizcategory={business_category}
                                descTitle="About us"
                                description={
                                    <span>
                                       Our clients generally have younger children, are tech savvy, 
                                       and entertain often. For these clients, home automation was/is a perfect fit. 
                                       They appreciate that they can check security cameras while they travel abroad, 
                                       see who is visiting upon arrival, receive notifications as their children come 
                                       and go, and—of course—it’s a huge bonus to be able to fully control their music, 
                                       lighting, and other features as they host events without ever leaving their guests’ 
                                       resence.
                                       Each project is 100% different and special in its own way. 
                                       Although I certainly have “my muses,” I’m proud to say that Control4 has 
                                       played a significant role in all of our builds.
                                    </span>
                                }
                                socials={
                                    <div>
                                        <Button simple><i className="fa fa-facebook-square"></i></Button>
                                        <Button simple><i className="fa fa-twitter"></i></Button>
                                        <Button simple><i className="fa fa-google-plus-square"></i></Button>
                                    </div>
                                }
                            />
                        </Col>
                        <div className="content">


                        <Col md={12}>
                            <Card
                                plain
                                title="Business Reviews"
                                category="We love to hear from you!"
                                ctTableFullWidth ctTableResponsive
                                content={



                       <form onSubmit={(event) => this.handleReviewFormSubmit(event)}> 
                             { this.state.reviews.map( //eslint-disable-next-line
                              (rev) => { 
                               
                               if(rev.business_name === business_name){
                                   return (
                                        <div className="typo-line">
                                            <p className="category">Reviews</p>
                                            <blockquote key={rev.id}>
                                             <p>
                                             {rev.review_text}
                                             </p>
                                             <small>
                                             @{rev.created_by}, <i>{rev.created_at}</i>
                                             </small>
                                            </blockquote>
                                        </div>
                                      )}
                                    }
                                )}
                            
                       <FormGroup controlId="formControlsTextarea" >
                          <ControlLabel>Please leave your review.</ControlLabel>
                              <FormControl 
                                  rows="5"
                                  name="review_text" 
                                  componentClass="textarea" 
                                  bsClass="form-control" 
                                  placeholder="Here can be your description" 
                                  value={this.state.formData.review_text}
                                  onChange= {this.handleFormChange}

                                />
                              </FormGroup>
                              <Button
                                  bsStyle="info"
                                  fill
                                  type="submit"
                                  >
                                  Submit Review
                              </Button>
                              </form>
                                }
                                />

                        </Col>
                    </div>
                </Grid>>
                
            </div>
            
        );
    }
}

export default Business;
