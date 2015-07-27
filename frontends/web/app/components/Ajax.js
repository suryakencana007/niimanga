var $ = require('jquery');
var Ajax = (function(){
    function Ajax() {}

    Ajax.prototype.normal = function (opts) {
        opts.dataType = 'json';
        return $.ajax(opts);
    };

    Ajax.prototype.authed = function (opts) {
        //var token = localStorage.getItem('token');
        opts.dataType = 'json';
        opts.headers = {
            'X-Token': "okey deh"
        };
        return $.ajax(opts);
    };

    Ajax.prototype.toAjax = function (opts) {
        return this.normal(opts);
    };
    return Ajax;
})();

var normalAjax = function (opts) {
    opts.dataType = 'json';
    return $.ajax(opts);
};

exports.toAjax = function (opts) {
    return normalAjax(opts);
};