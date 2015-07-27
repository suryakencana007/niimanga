var resolveHash = require('when/keys').all;

var fetchData = module.exports = (routerState) => {
  var { params, query } = routerState;
  return resolveHash(routerState.routes.filter((route) => {
    return route.handler.fetchData;
  }).reduce((promises, route) => {
    promises[route.name] = route.handler.fetchData(params, query);
    return promises;
  }, {}));
};