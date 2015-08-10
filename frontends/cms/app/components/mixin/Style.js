/** @flow */
var Radium = require('radium');
var swing = Radium.keyframes({
  '20%': {
    transform: 'rotate3d(0, 0, 1, 15deg)'
  },

  '40%': {
    transform: 'rotate3d(0, 0, 1, -10deg)'
  },

  '60%': {
    transform: 'rotate3d(0, 0, 1, 5deg)'
  },

  '80%': {
    transform: 'rotate3d(0, 0, 1, -5deg)'
  },

  '100%': {
    transform: 'rotate3d(0, 0, 1, 0deg)'
  }
});

var slideInDown = Radium.keyframes({
  '0%': {
    transform: 'translate3d(0, -100%, 0)',
    visibility: 'visible'
  },
  '100%': {
    transform: 'translate3d(0, 0, 0)'
  }
});

var bounceInDown = Radium.keyframes({
  '0%': {
    opacity: 0,
    transform: 'translate3d(0, -3000px, 0) scaleY(5)',
    transitionTimingFunction: 'cubic-bezier(0.215, 0.610, 0.355, 1.000)'
  },

  '60%': {
    opacity: 1,
    transform: 'translate3d(0, 25px, 0) scaleY(.9)',
    transitionTimingFunction: 'cubic-bezier(0.215, 0.610, 0.355, 1.000)'
  },

  '75%':{
    transform: 'translate3d(0, -10px, 0) scaleY(.95)',
    transitionTimingFunction: 'cubic-bezier(0.215, 0.610, 0.355, 1.000)'
  },

  '90%': {
    transform: 'translate3d(0, 5px, 0) scaleY(.985)',
    transitionTimingFunction: 'cubic-bezier(0.215, 0.610, 0.355, 1.000)'
  },

  '100%': {
    transform: 'none',
    transitionTimingFunction: 'cubic-bezier(0.215, 0.610, 0.355, 1.000)'
  }
});

module.exports = {
  animasi: {
    end: {
      animation: 'none 0s none',
      animationFillMode: 'both'
    },
    swing: {
      transformOrigin: 'top center',
      animation: swing + ' 1s infinite',
      animationFillMode: 'both'
    },
    slideInDown: {
      animation: slideInDown + ' 3s infinite',
      animationFillMode: 'both'
    },
    bounceInDown: {
      animation: bounceInDown + ' 3s infinite',
      animationFillMode: 'both'
    }
  }
}