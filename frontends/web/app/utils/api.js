var Promise = require('when').Promise;
var axios = require('axios');
var cache = require('./cache');

// var HOST = 'http://addressbook-api.herokuapp.com';
var HOST = '';
HOST = HOST+'/api/1.0';

exports.get = (url, token) => {
  var cached = cache.get(token, url);
  return (cached) ?
  Promise.resolve(cached) :
  axios({
    url: HOST+url,
    headers: [
    { 'Authorization': token }
    ]
  }).then(function(res) {
    cache.set(token, url, res.data);
    return res.data;
  }).catch(function (response) {
    if (response instanceof Error) {
      console.log('Error', response.message);
    } else {
      console.log(response.data);
      console.log(response.status);
      console.log(response.headers);
      console.log(response.config);

    }
    return {error: true};
  });
};

exports.post = (url, data, token) => {
  return axios({
    method: 'post',
    data: data,
    url: HOST+url,
    headers: [
    { 'Authorization': token }
    ]
  }).then(function(res) {
    return res.data;
  });
};
