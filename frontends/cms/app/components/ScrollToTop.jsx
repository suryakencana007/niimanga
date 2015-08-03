var React = require("react");
var Radium = require('radium');
var {Component, findDOMNode} = require('react');

@Radium.Enhancer
class ScrollToTop extends Component {
    componentDidMount() {
        this._attachListeners();
    }

    componentWillUnmount() {
        this._detachListeners();
    }

    _attachListeners() {
        var upBtn = findDOMNode(this.refs.upBtn);
        upBtn.addEventListener('webkitAnimationEnd', this._animEnd);
        upBtn.addEventListener('mozAnimationEnd', this._animEnd);
        upBtn.addEventListener('MSAnimationEnd', this._animEnd);
        upBtn.addEventListener('oanimationend', this._animEnd);
        upBtn.addEventListener('animationend', this._animEnd);
        window.addEventListener('scroll', this._update);

    }

    _detachListeners() {
        var upBtn = findDOMNode(this.refs.upBtn);
        upBtn.removeEventListener('webkitAnimationEnd', this._animEnd);
        upBtn.removeEventListener('mozAnimationEnd', this._animEnd);
        upBtn.removeEventListener('MSAnimationEnd', this._animEnd);
        upBtn.removeEventListener('oanimationend', this._animEnd);
        upBtn.removeEventListener('animationend', this._animEnd);
        window.removeEventListener('scroll', this._update);
    }

    _update = (e) => {
        if(getWindowScrollTop() > 100) {
            this.setState({isShow: true});
        } else {
            this.setState({isShow: false});
        }      
    };

    _animEnd = (e) => {
        this.setState({isAnimate: true});
    };

    _onClick() {
        window.scrollTo(0, 0);
    }

    _onScrollerMouseEnter = () => {
        this.setState({isHover: true});
    };

    _onScrollerMouseLeave = () => {
        this.setState({isHover: false});
    };

    render(): any {
        return (
            <div 
            onMouseEnter={this._onScrollerMouseEnter}
            onMouseLeave={this._onScrollerMouseLeave}
            ref="upBtn" style={[
                styles.css,
                (this.state.isAnimate) && styles.animEnd,
                (this.state.isShow) && styles.fadeIn,
                (!this.state.isShow) &&  styles.fadeOut,
                (this.state.isHover) && styles.swing,
                ]} onClick={this._onClick}>
                <a className="link">
                <span className="fa-stack fa-lg">
                <i className="fa fa-square fa-stack-2x"></i>
                <i className="fa fa-angle-double-up fa-stack-1x fa-inverse"></i>
                </span>
                </a>
                </div>);
    }
};

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

var styles = {
    animEnd: {
        animation: 'none 0s none'
    },
    css: {
        display: 'block',
        position: 'fixed',
        bottom: '10px',
        right: '10px'
    },
    fadeOut: {
        display: 'none'
    },
    fadeIn: {
        display: 'block',
        animation: bounceInDown + ' 1s both'
    },
    swing: {
        transformOrigin: 'top center',
        animation: swing + ' 1s both'
    }
};

function getWindowScrollTop() {
    if (window.pageYOffset !== undefined) {
        return window.pageYOffset;
    }

    var element: any =
    document.documentElement ||
    document.body.parentNode ||
    document.body;

    return element.scrollTop;
}

module.exports = ScrollToTop;