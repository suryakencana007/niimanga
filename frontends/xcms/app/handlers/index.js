/** @flow */

import React, {Component, PropTypes, findDOMNode } from 'react';
import { connect } from 'react-redux';
import { RouteHandler } from 'react-router';
import { resetErrorMessage, MessageBox } from '../actions';
import TransitionGroup from 'react/lib/ReactCSSTransitionGroup';
import MsgBox from 'components/MsgBox';
import Navbar from 'handlers/layouts/Navbar';
import Footer from 'handlers/layouts/Footer';
import Spinner from 'components/SpinnerUI';
import ScrollToTopBtn from 'components/ScrollToTop';


class App extends Component {
  constructor(props) {
    super(props);
    this._handleDismissClick = this._handleDismissClick.bind(this);
    this._renderErrorMessage = this._renderErrorMessage.bind(this);
    this.state = { loading: false};
  }

  componentDidMount() {
    this.props.MessageBox('let me show it');
    var timeout;
    this.props.loadingEvents.on('start', () => {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        this.setState({ loading: true });
      }, 500);
    });
    this.props.loadingEvents.on('end', () => {
      clearTimeout(timeout);
      this.setState({ loading: false });
    });
  }

  componentWillUnmount() {
    clearTimeout(this.pid);
  }

  _renderErrorMessage() {
    const { errorMessage } = this.props;
    if (!errorMessage) {
      return null;
    }

    return (<MsgBox onClick={this._handleDismissClick} 
      log={errorMessage.log} messageText={errorMessage.text} />);
  }

  _handleDismissClick(e) {
    this.props.resetErrorMessage();
  }

  render(): any {
    return (
      <div className="body">
      {this.state.loading ? <Spinner /> : null}
      <Navbar />
      <div className="content-wrapper" style={{ backgroundColor: '#fff'}}>
      {this._renderErrorMessage()}
      <TransitionGroup transitionName="tcontent">
      <RouteHandler key={name} {...this.props}/>
      </TransitionGroup>
      </div>
      <Footer />
      <ScrollToTopBtn />
      </div>
      );
  }
}

function mapStateToProps(state) {
  return {
    editors: state.editors,
    errorMessage: state.errorMessage
  }
}

export default connect(
  mapStateToProps,
  { resetErrorMessage, MessageBox }
  )(App);