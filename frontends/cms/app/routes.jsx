var React = require('react'),
Router = require('react-router'),
{ Route, DefaultRoute } = Router,
App = require('./pages'),
Index = require('./pages/home'),
Group = require('./pages/group'),
Series = require('./pages/manga'),
Chapter = require('./pages/chapter');


module.exports = () => {
    return [
    <Route handler={App}>
        <DefaultRoute handler={Index} />
        <Route name="group" path="/group" handler={Group} />
        <Route name="series" path="/series" handler={Series} />
        <Route name="chapter" path="/chapter" handler={Chapter} />
    </Route>
    ];
};