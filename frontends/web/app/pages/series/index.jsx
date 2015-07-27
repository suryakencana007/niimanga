var React = require('react'),
    Router = require('react-router'),
    { Link } = Router,
    ajax = require('components/Ajax'),
    Loading = require('components/Loading'),
    _ = require('lodash');

var Chapter_list = React.createClass({
    renderItem: function() {
        var chapters = _.map(this.props.chapters, function(chapter){
            var href = chapter.url.split('/');
            return (
                <Link to="chapter" params={{seriesSlug: href[0], chapterSlug: href[1]}} className="list-group-item">
                    {chapter.name} <span className="pull-right">{chapter.time}</span>
                </Link>
            )
        });
        return chapters;
    },
    render: function() {
        return (
            <div className="list-group">
             {this.renderItem()}
            </div>
        );
    }
});
var Pages = React.createClass({
    contextTypes: {
        router: React.PropTypes.func.isRequired
    },

    getInitialState: function() {
        return {
            series: null,
            populating: false
        };
    },

    getDefaultProps: function () {
        return {
            series: {
                "aka": "",
                "authors": [],
                "thumb_url": null,
                "name": "",
                "status": "",
                "description": [],
                "tags": [],
                "site": null,
                "time": null,
                "chapters": []
            },
            fetching: true
        };
    },

    componentDidMount: function() {
        var self = this;
        var params = this.context.router.getCurrentParams();
        ajax.toAjax({
            url: '/api/v1/series/' + params.seriesSlug,
            dataType: 'json',
            method: 'POST',
            success: function(data) {
                console.log(data.status);
                if (self.isMounted()) {
                    self.setState({
                        series: data,
                        populated: true
                    });
                }
            }.bind(self),
            error: function(data) {
                self.setState({
                    errorMsg: data.responseJSON.msg
                });
            },
            complete: function() {
                self.setState({fetching: false});
            }
        });
    },
    css: {
        padding: "10px 0"
    },

    renderTags: function(tags){
       return tags.map(function(item){
           return (<div className="ticket"><Link to="genre" params={{q: item.value}}><i className="fa fa-tag fa-lg fa-fw"></i>{item.label}</Link></div>);
       });
    },

    render: function() {
        var body;

        if(this.state.populated) {
            var series = this.state.series;
            var href = series.last_url.split('/');
            body = (
                <div className="col-md-12 card books page left-cover">
                    <div className="card-content">
                        <div className="cover">
                            <div className="cover-image-container">
                                <div className="cover-outer-align">
                                    <div className="cover-inner-align">
                                        <img className="cover-image"
                                            src={series.thumb_url}/>
                                    </div>
                                </div>
                            </div>
                            <div className="source-link" style={this.css}>
                                <a href={series.origin} target="_blank" className="btn btn-play"><i className="fa fa-link fa-fw"></i>Source</a>
                            </div>
                        </div>

                        <div className="detail">
                            <a className="title" href="#">{series.name}</a>

                            <div className="subtitle-container">
                                <a className="subtitle" href="#">{series.authors}</a>
                            </div>
                            <div className="alias">{series.aka}</div>
                            <div className="col-md-12 genres poros">
                                <div className="tengah">
                            {this.renderTags(series.tags)}
                                </div>
                            </div>
                            <div className="updated">{series.time}</div>
                            <div className="btn-ch">
                                <Link to="chapter" params={{seriesSlug: href[0], chapterSlug: href[1]}} className="btn btn-play">
                                    <i className="fa fa-leanpub fa-fw"></i>
                                {series.last_chapter}</Link>
                            </div>
                            <div className="description">
                                <p>
                            {series.description}
                                </p>
                            </div>
                        </div>
                    </div>
                    <div className = "title-green" > Chapters </div>
                    <Chapter_list chapters={series.chapters}/>
                </div>
            );
        } else {
            body = <Loading />;
        }
        return (
            <div className="row">
            {body}
            </div>

        );
    }
});

module.exports = React.createClass({
    render: function() {
        return (
            <div>
                <div className="container">
                    <Pages />
                </div>
            </div>
        );
    }
});