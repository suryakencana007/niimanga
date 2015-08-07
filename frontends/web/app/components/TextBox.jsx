var React = require("react");
var {Component} = require("react/addons");

class TextBox extends Component {
    render(): any {
        return (
            <input
            {...this.props}
            />
            );
    }
}
module.exports = TextBox;