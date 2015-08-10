/** @flow */

var React = require("react");
var Radium = require('radium');
var Colors = require('components/mixin/Colors');
var Style = require('components/mixin/Style');
var PureRender = require("components/mixin/PureRender");
var {Component, PropTypes} = require('react/addons');

@PureRender
@Radium.Enhancer
class Button extends Component {
  static propTypes = {
    children: PropTypes.node,
    onClick: PropTypes.func,
    type: React.PropTypes.string
  };

  static defaultProps = {
    type: 'button',
    color: 'base'
  };

  _onClick = (e: Object) => {
    this.props.onClick && this.props.onClick();
  };

  render(): any {
    return ( 
      <button
        onClick={this._onClick}
        type={this.props.type}
        style={[
          styles.base,
          this.props.color === 'red' && styles.red,
          this.props.style,
          Style.animasi.bounceInDown
        ]}>
        {this.props.children}
      </button>
    );
  }
}

var styles = {
  base: {
    fontSize: 16,
    backgroundColor: Colors.accent,
    color: "#fff",
    border: 0,
    borderRadius: "0.3em",
    padding: "0.4em 1em",
    cursor: "pointer",
    outline: "none",

    '@media (min-width: 992px)': {
      padding: "0.6em 1.2em"
    },

    '@media (min-width: 1200px)': {
      padding: "0.8em 1.5em"
    },

    ':hover': {
      backgroundColor: "#0088FF"
    },

    ':focus': {
      backgroundColor: "#0088FF"
    },

    ':active': {
      backgroundColor: "#005299",
      transform: "translateY(.1em)",
    }
  },

  red: {
    backgroundColor: "#d90000",

    ':hover': {
      backgroundColor: "#FF0000"
    },
    ':focus': {
      backgroundColor: "#FF0000"
    },
    ':active': {
      backgroundColor: "#990000"
    }
  }
};
module.exports = Button;