var tinycolor = require('tinytinycolor'),
_ = require('lodash');

var Color = (function(){
	function Color(stringOrColor) {
		this._color = new tinycolor(stringOrColor);
	}

	Color.prototype.toString = function () {
		return this._color.toHexString();
	};

	Color.prototype.darken = function (val) {
		return new Color(tinycolor.darken(this._color, val));
	};

	Color.prototype.lighten = function (val) {
		return new Color(tinycolor.lighten(this._color, val));
	};

	return Color;
})();
module.exports = Color;