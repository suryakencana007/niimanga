import { all } from 'when/keys';

module.exports = (token, routerState) => {
  var { params, query } = routerState;
  return all(routerState.routes.filter((route) => {
    return route.handler.fetchData;
  }).reduce((promises, route) => {
    promises[route.name] = route.handler.fetchData(token, params, query);
    return promises;
  }, {}));
};