var React = require('react');
var Router = require('react-router');
var { RouteHandler } = Router;
var TransitionGroup = require('react/lib/ReactCSSTransitionGroup');
var Navbar = require('pages/layouts/Navbar');
var Footer = require('pages/layouts/Footer');
var Spinner = require('components/Spinner');
var ScrollToTopBtn = require('components/ScrollToTop');


module.exports = React.createClass({
    getInitialState: function() {
      return {
        loading: false
      }
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

    render: function () {
     return (
        <div className="body-container">
        {this.state.loading ? <Spinner /> : null}
        <Navbar />

        <div className="content-wrapper" style={{ backgroundColor: '#fff'}}>
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