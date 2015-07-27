var $ = require('jquery');
var React = require("react");
module.exports = React.createClass({
    css: {
        position: 'fixed',
        bottom: '10px',
        right: '10px',
        display: 'none'
    },

    componentDidMount: function() {
        $(window).scroll(function() {
            if ($(this).scrollTop() > 100) {
                $('#up-btn').fadeIn();
            } else {
                $('#up-btn').fadeOut();
            }
        });
    },

    handleClick: function() {
        $('html, body').animate({scrollTop : 0}, 300);
    },

    render: function() {
        return (
            <div id="up-btn" style={this.css} onClick={this.handleClick}>
                <a className="link">
                    <span className="fa-stack fa-lg">
                        <i className="fa fa-square fa-stack-2x"></i>
                        <i className="fa fa-angle-double-up fa-stack-1x fa-inverse"></i>
                    </span>
                </a>
            </div>
        );
    }
});