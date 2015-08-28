/** @flow */

import React from 'react';
import { Route, DefaultRoute, NotFoundRoute } from'react-router';
import App from 'handlers';
import Index from 'handlers/Home';
import Group from 'handlers/Group';
import Series from 'handlers/Series';
import SeriesPage from 'handlers/Series/page';
import Chapters from 'handlers/Chapters';

module.exports = () => {
    return [
    <Route name="root" path="/cms" handler={App}>
        <DefaultRoute name="home" handler={Index} />
        <Route name="group" path="/cms/group" handler={Group} />
        <Route name="series" path="/cms/series" handler={Series} />
        <Route name="series_edit" path="/cms/series/:seriesSlug" handler={SeriesPage} />
        <Route name="chapters" path="/cms/chapters" handler={Chapters} />
        <Route name="genre" path="/cms/genres" handler={Chapters} />
        <Route name="chapter" path="/cms/genres" handler={Chapters} />
    </Route>
    ];
};