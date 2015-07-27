
var React = require('react');

module.exports = React.createClass({

    ribbonColor: function(source) {
        return "corner-ribbon top-right shadow " + source;
    },

    render: function() {
        var manga = this.props.manga;
        return (
            <div className="card books small left-cover">
                <div className="card-content">
                    <div className="wrapper-ribbon">
                        <div className={this.ribbonColor(manga.site)}>{manga.site}</div>
                    </div>
                    <div className="cover">
                        <div className="cover-image-container">
                            <div className="cover-outer-align">
                                <div className="cover-inner-align"><img className="cover-image"
                                    src={manga.thumb} /></div>
                            </div>
                        </div>
                    </div>
                    <div className="detail">
                        <a className="title" href="#">{manga.name}</a>

                        <div className="updated">{manga.time}</div>
                        <div className="btn-ch">
                            <a href="#" className="btn"><i className="fa fa-leanpub"></i>{manga.last_chapter.slice(0, 14)}</a>
                        </div>
                    </div>
                    <a href="#">
                        <span className="preview-overlay-container"></span>
                    </a>
                </div>
            </div>
        );
    }
});