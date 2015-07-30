var React = require('react'),
Router = require('react-router'),
{ Route, DefaultRoute } = Router,
App = require('./pages'),
Index = require('./pages/home'),
Latest = require('./pages/latest'),
Series = require('./pages/series'),
Chapter = require('./pages/series/chapter'),
Popular = require('./pages/popular'),
Genre = require('./pages/genre'),
Search = require('./pages/search');


module.exports = () => {
    return [
    <Route name="root" path="/" handler={App}>
        <DefaultRoute name="home" path="/" handler={Index} />
        <Route name="popular" path="/popular" handler={Popular} />
        <Route name="latest" path="/latest" handler={Latest} />
        <Route name="series" path="/manga/:seriesSlug" handler={Series} />
        <Route name="chapter" path="/chapter/:seriesSlug/:chapterSlug" handler={Chapter} />
        <Route name="search" path="/search/:q" handler={Search} />
        <Route name="genre" path="/genre/:q" handler={Genre} />
    </Route>
    ];
};