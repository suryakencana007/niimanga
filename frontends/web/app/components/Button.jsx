var React = require("react");
var PureRender = require("components/mixin/PureRender");
var {Component, PropTypes} = require('react/addons');

@PureRender
class Button extends Component {
  static propTypes = {
    children: PropTypes.node,
    onClick: PropTypes.func,
    types: React.PropTypes.string
  };

  static defaultProps = {
    types: 'button'
  };

  _onClick = (e: Object) => {
    this.props.onClick && this.props.onClick();
  };

  render(): any {


    return ( 
      <button
        onClick={this._onClick}
        type={this.props.type}>
        {this.props.children}
      </button>
    );
  }
}
module.exports = Button;