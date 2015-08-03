var React = require('react');
var Router = require('react-router');
var { RouteHandler } = Router;
var TransitionGroup = require('react/lib/ReactCSSTransitionGroup');
var Navbar = require('pages/layouts/Navbar');
var Footer = require('pages/layouts/Footer');
var ScrollToTopBtn = require('components/ScrollToTop');


module.exports = React.createClass({
    contextTypes: {
        router: React.PropTypes.func
    },
    render: function () {
     var name = this.context.router.getCurrentPath();
     return (
        <div className="body-container">

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