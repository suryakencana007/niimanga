var React = require('react'),
    Router = require('react-router'),
    { Route, DefaultRoute, RouteHandler, Link } = Router;

module.exports = React.createClass({
    render: function() {
        return (
            <footer className="footer-wrapper">
                <div className="container">
                    <div className="row">
                        <div className="footer-main">

                        </div>
                    </div>
                    <div className="row">
                        <div className="disclaimer">
                            Copyrights and trademarks for the manga, and other promotional materials are held by their respective owners and their use is allowed under the fair use clause of the
                            Copyright Law.
                            <div className="corporate">© 2015 Niimanga.net.</div>
                        </div>
                    </div>
                </div>
            </footer>
        );
    }
});