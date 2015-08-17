/**  @flow */

import React, {Component, PropTypes, findDOMNode} from 'react/addons';

export default class GooglePlus extends Component {

  componentDidMount(){
    var container = findDOMNode(this.refs.container);
    var gplus = document.createElement("script");
    gplus.id = "google-pjs";
    gplus.async = true;
    gplus.src = "https://apis.google.com/js/platform.js";
    if(!document.getElementById("google-pjs")){
      gplus.onload = this.renderWidget.bind(this);
      container.parentNode.appendChild(gplus);
    }
    else this.renderWidget();
  }

  componentWillUnmount(){
    if(this.props.cleanup) document.removeChild(document.getElementById("google-pjs"));
  }

  renderWidget(){
    if(this.props.type == "share"){
      
    }
  }

  render(){
    return <div ref="container" />
  }
}