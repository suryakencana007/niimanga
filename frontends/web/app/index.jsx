require('./styles.css');
require("font-awesome-webpack");

var React = require('react');
var Router = require('react-router');
var routes = require('./routes');
var fetchData = require('./utils/fetchData');
var rehydrate = require('./utils/rehydrate');
var { EventEmitter } = require('events');


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
    React.render(<Handler data={data} token={token} loadingEvents={loadingEvents} />, element);
  });
};

Router.run(routes(), Router.HistoryLocation, function (Handler, state) {
  renderState.Handler = Handler;
  renderState.routerState = state;
  render();
});