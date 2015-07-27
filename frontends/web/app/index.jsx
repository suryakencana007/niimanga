require('./styles.css');
require("font-awesome-webpack");

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