/**  @flow */

import React, {Component, PropTypes, findDOMNode} from 'react/addons';

export default class Twitter extends Component {

  componentDidMount(){
    var container = findDOMNode(this.refs.container);
    var twitter = document.createElement("script");
    twitter.id = "twitter-wjs";
    twitter.src = "//platform.twitter.com/widgets.js";
    if(!document.getElementById("twitter-wjs")){
      twitter.onload = this.renderWidget.bind(this);
      container.parentNode.appendChild(twitter);
    }
    else this.renderWidget();
  }

  componentWillUnmount(){
    if(this.props.cleanup) document.removeChild(document.getElementById("twitter-wjs"));
  }

  renderWidget(){
    if(this.props.type == "share"){
      twttr.widgets.createShareButton(
        this.props.url,
        findDOMNode(this.refs.container),
        {
          text: this.props.text
        }
        );
    }
  }

  render(){
    return <div ref="container" />
  }
}