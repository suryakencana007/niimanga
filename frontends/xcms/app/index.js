require('es6-shim');
require('./styles.css');
require("font-awesome-webpack");
require('bootstrap-table/dist/bootstrap-table.css');
require('bootstrap-table/dist/bootstrap-table.js');

import React from 'react';
import Router from 'utils/router';

import { Provider } from 'react-redux';
import configureStore from './store';

import fetchData from './utils/fetchData';
import rehydrate from './utils/rehydrate';
import { EventEmitter } from 'events';

const store = configureStore();

var loadingEvents = new EventEmitter();

var token = rehydrate();
var renderState = {
  element: document.getElementById('app-container'),
  Handler: null,
  routerState: null
};

var render = () => {
  var { element, Handler, routerState } = renderState;
  loadingEvents.emit('start');
  fetchData(token, routerState).then((data) => {
    loadingEvents.emit('end');
    React.render(
      <Provider store={store}> 
        { () => <Handler routerState={routerState} data={data} token={token} loadingEvents={loadingEvents} />}
      </Provider>
      , element);
  });
};

Router.run((Handler, state) => {
  renderState.Handler = Handler;
  renderState.routerState = state;
  render();
});