var React = require('react'),
    Router = require('react-router'),
    { RouteHandler } = Router,
    Navbar = require('pages/layouts/Navbar'),
    Footer = require('pages/layouts/Footer'),
    ScrollToTopBtn = require('components/ScrollToTop'),
    Spinner = require('components/Spinner');

module.exports = React.createClass({

    contextTypes: {
        router: React.PropTypes.func.isRequired
    },

    getInitialState: function() {
        return {
            isLoading: false
        };
    },

    componentWillMount: function() {
        this.setState({ isLoading: false });
    },

    componentDidMount: function() {
        var self = this;
        this.pid = setInterval(function(){
            self.setState({isLoading: false});
        }, 1000);
    },

    componentWillUnmount: function() {
        clearTimeout(this.pid);
    },

    isWrapper: function() {
        var wrapper = 'body-container';
        return wrapper;
    },

    upToComp: function() {
        // "Go to top" button.
        // Only show this on non-mobile devices where screen real estate is plenty
        if(! /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            return ScrollToTopBtn;
        }
    },

    render: function () {
        var activeCategory = this.context.router.getCurrentParams().category;
        return (
        <div className={this.isWrapper()}>
            {this.state.isLoading ? <Spinner /> : null}
            <Navbar />

            <div className="content-wrapper">
                <RouteHandler />
            </div>
            <Footer />
            <ScrollToTopBtn />
        </div>
        );
    }
});