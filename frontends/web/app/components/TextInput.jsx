var React = require("react");
module.exports = React.createClass({
    getInitialState: function() {
        return {value: ''};
    },

    handleChange: function(event) {
        this.setState({value: event.target.value});
    },

    render: function(e) {
        var type = this.props.type,
            placeholder = this.props.placeholder || '';

        return (<input type={type} onChange={this.handleChange}
            className="form-control" placeholder={placeholder} />);
    }
});