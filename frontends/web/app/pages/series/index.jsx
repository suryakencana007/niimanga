var React = require('react');
var Router = require('react-router');
var { Link } = Router;
var api = require('utils/api');
var HeadRender = require('components/mixin/HeadRender');
var Radium = require('radium');
var Loading = require('components/Loading');
var _ = require('lodash');

var isMobile = require('utils/ismobile');

var Chapter_list = React.createClass({
    renderItem: function() {
        var chapters = _.map(this.props.chapters, function(chapter){
            var href = chapter.url.split('/');
            return (
                <Link to="chapter" params={{seriesSlug: href[0], chapterSlug: href[1]}} className="list-group-item">
                <span>{chapter.name}</span><span className="pull-right">{chapter.time}</span>
                </Link>
            )
        });
        return chapters;
    },
    render: function() {
        return (
            <div className="col-xs-12 list-group">
             {this.renderItem()}
            </div>
        );
    }
});
var Pages = React.createClass({
    mixins: [HeadRender],
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
        var data = this.props.data.series;
        if (self.isMounted()) {
            self.setState({
                series: data,
                populated: true,
                head: {
                    title: data.name + " - Niimanga",
                    description: data.description + " " + data.tags.map(function(item){return item.label + " "}),
                    sitename: "Niimanga",
                    image: "http://niimanga.net/" + data.thumb_url,
                    url: "http://niimanga.net/#/manga/" + data.last_url.split('/')[0]
                }
            });
        }       
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
                <div className="card books page left-cover" style={(isMobile()? {display:'block'}: null)}>
                    <div className="card-content">
                        <div className="col-md-2 col-xs-12 cover">
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

                        <div className="col-md-10 col-xs-12 detail">
                            <a className="title" href="#">{series.name}</a>

                            <div className="col-xs-12 subtitle-container">
                                <a className="subtitle" href="#">{series.authors}</a>
                            </div>
                            <div className="col-xs-12 alias">{series.aka}</div>
                            <div className="col-xs-12 genres poros">
                                <div className="tengah">
                            {this.renderTags(series.tags)}
                                </div>
                            </div>
                            <div className="col-xs-12 updated">{series.time}</div>
                            <div className="col-xs-12 btn-ch">
                                <Link to="chapter" params={{seriesSlug: href[0], chapterSlug: href[1]}} className="btn btn-play">
                                    <i className="fa fa-leanpub fa-fw"></i>
                                {series.last_chapter}</Link>
                            </div>
                            <div className="col-xs-12 description">
                                <p>
                            {series.description}
                                </p>
                            </div>
                        </div>
                    </div>
                    <div className="title-green" > Chapters </div>
                    <Chapter_list chapters={series.chapters}/>
                </div>
            );
        } else {
            body = <Loading />;
        }
        return (
            <div className="row">
            {this.renderHead()}
            {body}
            </div>
        );
    }
});

var styles = {
    left: {
        height: '900px',
        left: '-493px',
        top: '34px',
        position: 'fixed',
        width: '50%',
        cursor: 'pointer',
        background: 'url(/static/res/ad-banner-left.png) 100% 0% no-repeat scroll transparent'
    },

    right: {
        height: '900px',
        left: '711px',
        top: '34px',
        position: 'fixed',
        width: '50%',
        cursor: 'pointer',
        background: 'url(/static/res/ad-banner-right.png) 100% 0% no-repeat scroll transparent'
    }
};

module.exports = React.createClass({
     statics: {
        fetchData: function(token, params, query) {
            var url = '/series/' + params.seriesSlug;
            return api.post(url, token).then(null ,
                function(){
                    return {error: true};
                });
        }
    },

    render: function() {
        return (
            <div>
                <div className="container">
                {isMobile() ? null: <span>
                   <a ref="ad-left" href="#"><div style={styles.left}></div></a>
                   <a ref="ad-right" href="#"><div style={styles.right}></div></a>
                   </span>
               }
               <Pages {...this.props}/>
                </div>
            </div>
        );
    }
});