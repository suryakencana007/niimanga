'use strict';
require('./styles.css');
require("font-awesome-webpack");
require('X-editable/dist/bootstrap3-editable/css/bootstrap-editable.css');
require('X-editable/dist/bootstrap3-editable/js/bootstrap-editable.js');
require('bootstrap-table/dist/bootstrap-table.css');
require('bootstrap-table/dist/bootstrap-table.js');
require('bootstrap-table/dist/extensions/editable/bootstrap-table-editable.js');

var React = require('react'),
Router = require('react-router'),
routes = require('./routes');

var renderState = {
  element: document.getElementById('app-container'),
  Handler: null,
  routerState: null
};

var render = () => {
  var { element, Handler, routerState } = renderState;
  React.render(<Handler />, element);
};

Router.run(routes(), function (Handler, state) {
  renderState.Handler = Handler;
  renderState.routerState = state;
  render();
});