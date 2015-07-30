var React = require("react");
var PureRender = require("components/mixin/PureRender");
var {Component} = require("react/addons");

@PureRender
class TextBox extends Component {
    render(): any {
        return (
            <input 
            className="form-control"
            {...this.props}
            />
            );
    }
}
module.exports = TextBox;