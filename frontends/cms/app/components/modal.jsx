var React = require("react");
var $ = require('jquery');

module.exports = React.createClass({
    render: function() {
        var title = this.props.title || 'Title Form';

        return (
            <div className="modal fade" tabIndex="-1" role="dialog" aria-hidden="true">
                <div className="modal-dialog modal-md">
                    <div className="modal-content">
                        <div className="modal-header">
                            <div style={this.css} ><button type="button" className="close" data-dismiss="modal">
                                <span aria-hidden="true">&times;</span>
                                <span className="sr-only">Close</span>
                            </button></div>
                            <div className="title-green">{title}</div>
                        </div>
                        <div className="modal-body">
                    {this.renderBody(this.props.body)}
                        </div>
                        <div className="modal-footer">
                            <div className="row">
                                <div className="col col-md-12">
                                    <button type="button" className="btn btn-primary pull-right" onClick={this.save}>Save</button>
                                    <button type="button" className="btn btn-default pull-right spacing-right" onClick={this.reset} data-dismiss="modal">Close</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    },

    css: {
        marginBottom: '27px'
    },

    getInitialState: function() {
        return {
            visible: false
        };
    },

    componentDidMount: function () {
        this.$el = $(React.findDOMNode(this));
        this.$el.on("hidden.bs.modal", this.reset);

        //emitter.on(constants.changed, function() {
        //    this.$el.modal("hide");
        //}.bind(this));
    },

    componentWillUnmount: function() {
        //emitter.off(constants.changed);
    },

    show: function () {
        this.$el.modal("show");
    },

    close: function () {
        this.$el.modal("hide");
    },

    reset: function() {
        if(this.props.reset) this.props.reset();
    },

    save: function() {
        if(this.props.save) this.props.save();
    },

    renderBody: function(c) {
        return React.createElement(c, {});
    }
});