/** @flow */

var React = require("react");
var Radium = require('radium');
var PureRender = require("components/mixin/PureRender");
var {Component} = require("react/addons");

@PureRender
@Radium.Enhancer
class Input extends Component {
  static propTypes = {
    onChange: PropTypes.func,
    type: React.PropTypes.string
  };

  static defaultProps = {
    type: 'text'
  };

  _onChange = (e: Object) => {
    this.props.onChange && this.props.onChange();
  };

  render(): any {
    return (<input 
      type={this.props.type}
      onChange={this._onChange}/>);
  }
}

var styles = {
  
}
module.exports = Input;