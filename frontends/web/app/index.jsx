require('./styles.css');
require("font-awesome-webpack");

var React = require('react');
var Router = require('react-router');
var routes = require('./routes');
var fetchData = require('./utils/fetchData');
var EventEmitter = require('events').EventEmitter;


var loadingEvents = new EventEmitter();

var renderState = {
  element: document.getElementById('app-container'),
  Handler: null,
  routerState: null
};

var render = () => {
  var { element, Handler, routerState } = renderState;
  loadingEvents.emit('start');
  fetchData(routerState).then((data) => {
    loadingEvents.emit('end');
    React.render(<Handler data={data} loadingEvents={loadingEvents} />, element);
  });
};

Router.run(routes(), function (Handler, state) {
  renderState.Handler = Handler;
  renderState.routerState = state;
  render();
});