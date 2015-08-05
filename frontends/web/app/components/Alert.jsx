var React = require("react");
module.exports = React.createClass({
    render: function() {
        if (!this.props.msg) {
            return (<span></span>);
        }

        if (this.props.hasOwnProperty('cssClass')) {
            var cssClass = this.props.cssClass;
        } else {
            var cssClass = 'danger';
        }

        var className = "alert alert-" + cssClass;

        if (this.props.hasOwnProperty('dismissible') &&
            this.props.dismissible === "true") {
            return (
                <div className={className + ' alert-dismissible'} role="alert" style={{marginTop: '10px'}}>
                    <button type="button" className="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    {this.props.msg}
                </div>
            );
        }

        return (
            <div className={className} role="alert" style={{marginTop: '10px'}}>{this.props.msg}</div>
        );
    }
});