var React = require('react');

module.exports = React.createClass({
    css: {       
        width: 'auto',
        margin: 0
    },
    secHeader: {
        overflow: 'hidden',
        'margin-bottom': '20px'
    },

    render: function() {
        return (
            <div id="cover-anime-sl" className="card-content carousel slide" data-ride="carousel">
                <div className="section-feature">
                        <ol className="carousel-indicators slider-nav">
                            <li data-target="#cover-anime-sl" data-slide-to="0" className="active"></li>
                            <li data-target="#cover-anime-sl" data-slide-to="1"></li>
                            <li data-target="#cover-anime-sl" data-slide-to="2"></li>
                            <li data-target="#cover-anime-sl" data-slide-to="3"></li>
                        </ol>
                        <div className="carousel-inner" role="listbox">
                            <div className="item active">
                                <img src="static/res/besar-4.1.jpg" className="img-responsive" />
                                <div className="carousel-caption">
                                    <span className="glyphicon glyphicon-eye-open" aria-hidden="true"></span>
                                    <span className="sr-only">12</span>
                                </div>
                            </div>
                            <div className="item">
                                <img src="static/res/besar-4.2.jpg" className="img-responsive" />
                                <div className="carousel-caption">
                                    <span className="fa fa-eye fa-fw" aria-hidden="true"></span>
                                    <span className="sr-only">23</span>
                                </div>
                            </div>
                            <div className="item">
                                <img src="static/res/besar-5.2.jpg" className="img-responsive" />
                                <div className="carousel-caption">
                                    <span className="fa fa-eye fa-fw" aria-hidden="true"></span>
                                    <span className="sr-only">23</span>
                                </div>
                            </div>
                            <div className="item">
                                <img src="static/res/besar-5.1.jpg" className="img-responsive" />
                                <div className="carousel-caption">
                                    <span className="fa fa-eye fa-fw" aria-hidden="true"></span>
                                    <span className="sr-only">23</span>
                                </div>
                            </div>
                        </div>
                    
                </div>
            </div>
        );
    }
});