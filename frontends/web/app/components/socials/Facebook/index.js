/**  @flow */

import React, {Component, PropTypes, findDOMNode} from 'react/addons';

export default class Facebook extends Component {

  componentDidMount(){
    var container = findDOMNode(this.refs.container);
    var facebook = document.createElement("script");
    facebook.id = "facebook-jssdk";
    facebook.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.4&appId=844212729007674";
    if(!document.getElementById("facebook-jssdk")){
      facebook.onload = this.renderWidget.bind(this);
      container.parentNode.appendChild(facebook);
    }
    else this.renderWidget();
  }

  componentWillUnmount(){
    if(this.props.cleanup) {
      var container = findDOMNode(this.refs.container);
      container.parentNode.removeChild(document.getElementById("facebook-jssdk"));
    }
  }

  renderWidget(){
    if(this.props.type == "share"){
        FB.init({
          appId      : '844212729007674',
          xfbml      : true,
          version    : 'v2.4'
        });
    }
  }

  render(){
    return <div ref="container" />
  }
}