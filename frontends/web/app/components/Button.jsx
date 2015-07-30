var React = require("react");
var PureRender = require("components/mixin/PureRender");
var {Component, PropTypes} = require('react/addons');

@PureRender
class Button extends Component {
  static propTypes = {
    children: PropTypes.node,
    onClick: PropTypes.func,
    use: PropTypes.oneOf(['default', 'special'])
  }

  static defaultProps = {
    use: 'default'
  };

  _onClick = () => {
    this.props.onClick && this.props.onClick();
  };

  render(): any {
    return (
      <button
        onClick={this._onClick}
        type="button">
        {this.props.children}
      </button>
    );
  }
}