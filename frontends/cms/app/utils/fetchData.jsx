var resolveHash = require('when/keys').all;

module.exports = (token, routerState) => {
  var { params, query } = routerState;
  return resolveHash(routerState.routes.filter((route) => {
    return route.handler.fetchData;
  }).reduce((promises, route) => {
    promises[route.name] = route.handler.fetchData(token, params, query);
    return promises;
  }, {}));
};