import React, {Component, PropTypes} from 'react/addons';
import Carousel from 'nuka-carousel';

var Slickers = React.createClass({
  mixin:[Carousel.ControllerMixin],
  render(): any {
    return (
      <Carousel>
        <img src="static/res/besar-4.1.jpg" className="img-responsive" />
        <img src="static/res/besar-4.2.jpg" className="img-responsive" />
        <img src="static/res/besar-5.1.jpg" className="img-responsive" />
        <img src="static/res/besar-5.2.jpg" className="img-responsive" />
      </Carousel>
      );
  }
});

module.exports = Slickers;