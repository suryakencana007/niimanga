var React = require('react');
var Router = require('react-router');
var { RouteHandler } = Router;
var GoogleAnalytics = require('react-g-analytics');
var api = require('utils/api');
var HeadRender = require('components/mixin/HeadRender');
var Navbar = require('pages/layouts/Navbar');
var Footer = require('pages/layouts/Footer');
var TransitionGroup = require('react/lib/ReactCSSTransitionGroup');
var ScrollToTopBtn = require('components/ScrollToTop');
var Spinner = require('components/Spinner');
var Sidebar = require('pages/layouts/Sidebar');

var isMobile = require('utils/ismobile');

module.exports = React.createClass({
    mixins: [HeadRender],
    contextTypes: {
        router: React.PropTypes.func.isRequired
    },
    statics: {
        fetchData: function(token, params, query) {
            return api.get('api/v1/genres?q=', token).then(function(data){
                return Array.prototype.slice.call(data.rows, 0, data.rows.length);
            }).then(null , function(){
                return {error: true};
            });
        }
    },

    getInitialState: function() {
        return {
            isLoading: false,
            genres: undefined
        };
    },

    componentWillMount: function() {
        // this.fetchGenres();
    },

    componentDidMount: function() {
        var timeout;
        this.props.loadingEvents.on('start', () => {
          clearTimeout(timeout);
          timeout = setTimeout(() => {
            this.setState({ loading: true });
        }, 250);
      });
        this.props.loadingEvents.on('end', () => {
          clearTimeout(timeout);
          this.setState({ loading: false });
      });    
    },

    componentWillUnmount: function() {
        clearTimeout(this.pid);
    },

    fetchGenres: function() {
        var data = api.get('api/v1/genres?q=', this.props.token).then(function(data){
            return Array.prototype.slice.call(data.rows, 0, data.rows.length);
        }).then(null , function(){
            return {error: true};
        });
        if(!data.error) this.setState({genres: data});
    },

    render: function () {
        var data = this.props.data.root;
        return (
            <span>
             {!isMobile() ? null: <Sidebar />}
            <div className={!isMobile() ? 'body-container': 'content-wrapper-mobile'}>
            {this.state.loading ? <Spinner /> : null}
            <Navbar genres={data}/>

            <div className="content-wrapper" style={isMobile()? {padding: 0}: null}>
            <GoogleAnalytics id="UA-65629589-1" />
            <TransitionGroup transitionName="tcontent">
            <RouteHandler key={name} {...this.props}/>
            </TransitionGroup>
            </div>
            <Footer />
            <ScrollToTopBtn />
            </div>
            </span>
            );
    }
});