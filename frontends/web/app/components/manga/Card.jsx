var React = require('react'),
    Router = require('react-router'),
    { Link } = Router;

module.exports = React.createClass({

    ribbonColor: function(source) {
        return "corner-ribbon top-right shadow " + source;
    },

    render: function() {
        var manga = this.props.manga;
        var href = manga.last_url.split('/');
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
                        <Link to="series" params={{seriesSlug: manga.origin}} >
                            <span className="preview-overlay-container"></span>
                        </Link>
                    </div>
                    <div className="detail">
                        <Link to="series" params={{seriesSlug: manga.origin}} className="title">{manga.name}</Link>

                        <div className="updated">{manga.time}</div>
                        <div className="btn-ch">
                            <Link to="chapter" params={{seriesSlug: href[0], chapterSlug: href[1]}} className="btn btn-play"><i className="fa fa-play fa-fw"></i>{manga.last_chapter.slice(0, 14)}</Link>
                        </div>
                    </div>

                </div>
            </div>
        );
    }
});