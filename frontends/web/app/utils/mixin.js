var assign = require('object-assign');

module.exports.Mixin = function Mixin(...mixins) {
  var Class = function(...args) {
    mixins.forEach((mixin) =>
      mixin.constructor && mixin.constructor.call(this, ...args)
    );
  };

  assign(Class.prototype, ...mixins);

  return Class;
};