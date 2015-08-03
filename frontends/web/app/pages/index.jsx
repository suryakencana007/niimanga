var React = require('react');
var Router = require('react-router');
var { RouteHandler } = Router;
var GoogleAnalytics = require('react-g-analytics');
var ajax = require('components/Ajax');
var HeadRender = require('components/mixin/HeadRender');
var Navbar = require('pages/layouts/Navbar');
var Footer = require('pages/layouts/Footer');
var TransitionGroup = require('react/lib/ReactCSSTransitionGroup');
var ScrollToTopBtn = require('components/ScrollToTop');
var Spinner = require('components/Spinner');

module.exports = React.createClass({
    mixins: [HeadRender],
    contextTypes: {
        router: React.PropTypes.func.isRequired
    },

    getInitialState: function() {
        return {
            isLoading: false,
            genres: undefined
        };
    },

    componentWillMount: function() {
        this.setState({ isLoading: false });
        this.fetchGenres();
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

    fetchGenres: function() {
        var self = this;
        ajax.toAjax({
            url: "api/v1/genres?q=",
            dataType: 'json',
            method: 'GET',
            success: function (data) {
             
                data =  Array.prototype.slice.call(data.rows, 0, data.rows.length);
                self.setState({genres: data})
            }.bind(self),
            error: function (data) {
              
                console.log(data);
            }.bind(self),
            complete: function () {
                self.setState({fetching: false});
            }.bind(self)
        });
    },

    render: function () {
        return (
            <div className={this.isWrapper()}>
            {this.state.isLoading ? <Spinner /> : null}
            <Navbar genres={this.state.genres}/>

            <div className="content-wrapper">
            <GoogleAnalytics id="UA-65629589-1" />
            <TransitionGroup transitionName="tcontent">
            <RouteHandler key={name} {...this.props}/>
            </TransitionGroup>
            </div>
            <Footer />
            <ScrollToTopBtn />
            </div>
            );
    }
});