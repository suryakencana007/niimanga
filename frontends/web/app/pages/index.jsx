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

var injectTapEventPlugin = require('react-tap-event-plugin');
var SideBarUI = require('components/SideBar');
var isMobile = require('utils/ismobile');

injectTapEventPlugin();

module.exports = React.createClass({
    mixins: [HeadRender],
    contextTypes: {
        router: React.PropTypes.func.isRequired
    },
    statics: {
        fetchData: function(token, params, query) {
            return api.get('/genres?q=', token).then(function(data){
                return Array.prototype.slice.call(data.rows, 0, data.rows.length);
            }).then(null , function(){
                return {error: true};
            });
        }
    },

    getInitialState: function() {
        return {
            isLoading: false,
            genres: undefined,
            docked: false,
            open: false,
            transitions: true,
            touch: true,
            touchHandleWidth: 20,
            dragToggleDistance: 30,
            ismobile: false
        };
    },

    onSetOpen(open) {
        this.setState({open: open});
    },

    menuButtonClick(ev) {
        ev.preventDefault();
        this.onSetOpen(!this.state.open);
    },

    componentWillMount: function() {
      this.setState({ismobile: isMobile() });
    },
    
    componentDidMount: function() {
        var timeout;
        this.props.loadingEvents.on('start', () => {
          clearTimeout(timeout);
          timeout = setTimeout(() => {
            this.setState({ loading: true });
        }, 500);
      });
        this.props.loadingEvents.on('end', () => {
          clearTimeout(timeout);
          this.setState({ loading: false });
      });
    },

    componentWillUnmount: function() {
        clearTimeout(this.pid);
    },

    render: function () {
        var data = this.props.data.root;
        var sidebar = <Sidebar />;
        var sidebarProps = {
          sidebar: sidebar,
          docked: this.state.docked,
          open: this.state.open,
          touch: this.state.touch,
          touchHandleWidth: this.state.touchHandleWidth,
          dragToggleDistance: this.state.dragToggleDistance,
          transitions: this.state.transitions,
          onSetOpen: this.onSetOpen,
        };
         var contentHeader = (
          <span>
            {!this.state.docked &&
             <a className="menu-trigger" onClick={this.menuButtonClick} href="#"> <i className="fa fa-bars fa-fw"></i></a>}
          </span>);
         

        var body = (
            <div className={!this.state.ismobile ? 'body-container': 'content-wrapper-mobile'}>
            {this.state.loading ? <Spinner /> : null}
            <Navbar genres={data} menuBar={contentHeader}/>

            <div className="content-wrapper" style={this.state.ismobile? {padding: 0}: null}>
            <GoogleAnalytics id="UA-65629589-1" />
            <TransitionGroup transitionName="tcontent">
            <RouteHandler key={name} {...this.props}/>
            </TransitionGroup>
            </div>
            <Footer />
            <ScrollToTopBtn />
            </div>
            );

        body = this.state.ismobile ? (
            <SideBarUI {...sidebarProps}>
                {body}
            </SideBarUI>
            ): (body);
        return (
            <span>{body}</span>
            );
    }
});