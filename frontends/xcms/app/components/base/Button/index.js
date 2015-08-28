/** @flow */

import React, {Component, PropTypes} from 'react/addons';
import Radium from 'radium';
import Colors from 'components/mixin/Colors';
import PureRender from 'components/mixin/PureRender';

@PureRender
@Radium.Enhancer
class Button extends Component {
  _onClick(e: Object) {
    this.props.onClick && this.props.onClick();
  };

  render(): any {
    return ( 
      <button
      onClick={this._onClick.bind(this)}
      type={this.props.type}
      style={[
        styles.base,
        this.props.color === 'red' && styles.red,
        this.props.style]}>
        {this.props.children}
        </button>
        );
  }
}

var styles = {
  base: {
    fontSize: '12px',
    fontFamily: 'inherit',
    fontWeight: 'inherit',
    backgroundColor: Colors.primary,
    color: Colors.white,
    border: 0,
    borderRadius: "0.3em",
    padding: "0.4em 1em",
    cursor: "pointer",
    outline: "none",

    '@media (min-width: 992px)': {
      padding: "0.6em 1.2em"
    },

    '@media (min-width: 1200px)': {
      padding: "0.8em 1.4em"
    },

    ':hover': {
      backgroundColor: Colors.primary.lighten(5)
    },

    ':focus': {
      backgroundColor: Colors.primary
    },

    ':active': {
      backgroundColor: Colors.primary
    }
  },

  red: {
    backgroundColor: Colors.red,

    ':hover': {
      backgroundColor: Colors.red.lighten(5)
    },
    ':focus': {
      backgroundColor: Colors.red
    },
    ':active': {
      backgroundColor: Colors.red
    }
  }
};

Button.propTypes = {
  children: PropTypes.node,
  onClick: PropTypes.func,
  type: React.PropTypes.string
};

Button.defaultProps = {
  type: 'button',
  color: 'base'
};

export default Button;