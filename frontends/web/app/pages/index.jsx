var React = require('react'),
    Router = require('react-router'),
    { RouteHandler } = Router,
    // GoogleAnalytics = require('react-g-analytics'),
    ajax = require('components/Ajax'),
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
                //cached.set('chapter_' + url, data);
                // console.log(data.rows);
                data =  Array.prototype.slice.call(data.rows, 0, data.rows.length);
                self.setState({genres: data})
            }.bind(self),
            error: function (data) {
                //self.setState({
                //    errorMsg: data.responseJSON.msg
                //});
                console.log(data);
            }.bind(self),
            complete: function () {
                self.setState({fetching: false});
            }.bind(self)
        });
    },

    render: function () {
        var activeCategory = this.context.router.getCurrentParams().category;       
        // <GoogleAnalytics id="UA-65629589-1" />
        return (
        <div className={this.isWrapper()}>
            {this.state.isLoading ? <Spinner /> : null}
            <Navbar genres={this.state.genres}/>

            <div className="content-wrapper">
                
                <RouteHandler />
            </div>
            <Footer />
            <ScrollToTopBtn />
        </div>
        );
    }
});