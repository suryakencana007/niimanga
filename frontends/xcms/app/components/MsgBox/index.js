/**  @flow */

import React, {Component, PropTypes, findDOMNode} from 'react/addons';
import Radium from 'radium';
import Colors from 'components/mixin/Colors';
import PureRender from 'components/mixin/PureRender';

@PureRender
@Radium.Enhancer
export default class MsgBox extends Component {
  static propTypes = {
    messageText:PropTypes.string,
    onClick: PropTypes.func,
    log: PropTypes.string
  }

  constructor() {
    super();
    this._onClick = this._onClick.bind(this);
  }

  _onClick(e: object) {
    this.props.onClick && this.props.onClick();
  }

  render(): any {
    if (!this.props.messageText) {
      return null;
    }
    return (
     <p onClick={this._onClick} style={[
      styles.base,
      this.props.log === 'alert' && styles.alert,
      this.props.log === 'info' && styles.info,
      this.props.log === 'warn' && styles.warn,
      this.props.log === 'debug' && styles.debug
      ]}>
      <b>{this.props.messageText}</b>
      {' '}
      <span style={styles.btn} >
      <i className="fa fa-close fa-inverse fa-fw"></i>
      </span>
      </p>);
  }
}

let styles = {
  base: {
    position: 'relative',
    color: Colors.white,
    textAlign: 'center',
    padding: '10px',
    fontSize: '14px',
    backgroundColor: Colors.pink,
    ':hover': {
      color: Colors.primary,
      cursor: 'pointer',
      backgroundColor: Colors.gray
    }
  },
  alert: {
    backgroundColor: Colors.red
  },
  info: {
    backgroundColor: Colors.blue
  },
  warn: {
    backgroundColor: Colors.yellow
  },
  debug: {
    backgroundColor: Colors.indigo
  },
  btn: {
    float: 'left'
  }
};
