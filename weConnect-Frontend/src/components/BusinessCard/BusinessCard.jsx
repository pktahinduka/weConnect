import React, { Component } from 'react';

export class BusinessCard extends Component{

    render(){
        return (
            <div className="card card-user">
                <div className="image" style={{ height:'200px' }}>
                    <img src={this.props.bgImage} alt="..."/>
                </div>
                <div className="content">
                    <div className="author">
                         <a href="#pablo">
                            <img className="avatar border-gray" 
                            style={{ marginRight:'80%', 
                                     height:'160px', 
                                     width:'160px',
                                     marginTop:'-3%',
                                     borderColor:'#2B9ACE' }} 
                            src={this.props.avatar} alt="..."/>
                            <h4 className="title text-left" style={{ marginLeft:'20px' }}>
                                <h4><b>{this.props.role}</b></h4>
                                <small>{this.props.userName}</small> 
                                <br />
                                {this.props.name}
                                
                                <br /><br />
                                <small>{this.props.category}</small> 
                                <br />
                                {this.props.bizcategory}
                                
                            </h4>
                        </a>
                    </div>
                    <p className="description text-left" style={{ marginLeft:'20px', marginRight:'20px'  }}>
                        <br />
                        <h4 className="title text-left">
                        <small>{this.props.descTitle}</small>
                        </h4> 
                        <i>{this.props.description}</i>
                    </p>
                </div>
                <hr />

                <div className="text-center">
                    {this.props.socials}
                </div>
            </div>
        );
    }
}

export default BusinessCard;
