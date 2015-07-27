
var React = require('react');

var oldCard = React.createClass({
    render: function() {
        return (
            <div>
                <div className="card anime-mob">
                    <div className="wrapper-ribbon">
                        <div className="corner-ribbon top-right red shadow">batoto</div>
                    </div>
                    <a className="link-cover" href="#">
                        <span className="cover">
                            <img src="static/res/cover-nanatsu.jpg" className="img-responsive" />
                        </span>
                        <div className="cover-info">
                            <p className="title">Fairy Tail</p>
                        </div>
                    </a>
                    <div className="feat-info">
                        <a href="#" className="btn btn-default white-btn">
                            Episode 001
                            <i className="fa fa-play"></i>
                        </a>

                    </div>
                </div>
            </div>
        );
    }
});

module.exports = React.createClass({

    ribbonColor: function(source) {
        return "corner-ribbon top-right shadow " + source;
    },

    render: function() {
        var manga = this.props.manga;
        return (
            <div className="card books small tall-cover">
                <div className="card-content">
                    <div className="wrapper-ribbon">
                        <div className={this.ribbonColor(manga.site)}>{manga.site}</div>
                    </div>
                    <div className="cover">
                        <div className="cover-image-container">
                            <div className="cover-outer-align">
                                <div className="cover-inner-align">
                                    <img className="cover-image"
                                        src={manga.thumb} /></div>
                            </div>
                        </div>
                        <a href="#">
                            <span className="preview-overlay-container"></span>
                        </a>
                    </div>
                    <div className="detail">
                        <a className="title" href="#">{manga.name}</a>

                        <div className="updated">{manga.time}</div>
                        <div className="btn-ch">
                            <a href="#" className="btn btn-play"><i className="fa fa-play"></i>{manga.last_chapter.slice(0, 14)}</a>
                        </div>
                    </div>

                </div>
            </div>
        );
    }
});