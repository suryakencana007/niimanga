var React = require('react');
var Router = require('react-router');
var { Link } = Router;
var api = require('utils/api');
var Loading = require('components/Loading');
var Alert = require('components/Alert');

var Pages = React.createClass({

    // Max number of pages to load concurrently
    NUM_CONCURRENT: 3,

    getInitialState: function () {
        return {
            loaded: []
        };
    },

    componentWillReceiveProps: function (nextProps) {

        if (nextProps.imgs.length > 0) {

            // Leave pages as-is if already rendered
            var loaded = this.state.loaded;
            if (loaded.length > 0 && loaded[0] === nextProps.imgs[0]) {
                return;
            }

            // Render first image which has an onLoad event handler which
            // renders the second image which has an onload event handler to
            // render the third image... and so on.
            this.setState({
                loaded: nextProps.imgs.slice(0, this.NUM_CONCURRENT)
            });

        } else {
            // Clean up when changed to another chapter
            this.setState({
                loaded: []
            });
        }
    },

    render: function () {
        var all = this.props.imgs;
        var loaded = this.state.loaded;
        var self = this;

        var images = loaded.map(function (url, index) {

            // function to append the next NUM_CONCURRENT images into the DOM
            // when this image has finished loading:
            var appendFunc = function () {
                for (var i = 1, len = self.NUM_CONCURRENT; i <= len; i++) {
                    var nextIndex = index + i;
                    var nextImgUrl = all[nextIndex];

                    if (nextIndex < all.length) {
                        if (loaded.indexOf(nextImgUrl) === -1) {
                            loaded.push(nextImgUrl);
                        }
                    } else {
                        break;
                    }
                }

                self.setState({loaded: loaded});
            };
            return (
                <div className="col-xs-12 col-md-12 col-sm-12">
                  
                        <div className="card-content" style={{marginBottom: '10px'}}>
                            <img className="img-responsive" key={url + index} src={url}
                                onLoad={appendFunc} />
                            <div className="page-number">{ index + 1 } / { all.length }</div>
                        </div>
                  
                </div>
            );
        });
        return (
            <div className="chapter-image">
                {images}
                <Loading loading={all.length > loaded.length} />
            </div>
        );
    }
});

module.exports = React.createClass({

    statics: {
        fetchData: function(token, params, query) {
            var url = '/chapter/' + params.seriesSlug + '/' + params.chapterSlug;
            return api.post(url, token).then(null ,
                function(){
                    return {error: true};
                });
        }
    },

    render: function () {
        var data = this.props.data.chapter;
        var info = this.state.info,
            name = info.name,
            next = info.next_chapter_url,
            prev = info.prev_chapter_url,
            fetching = this.state.fetching;

        var pages = <Pages imgs={info.pages} />;

        var setState = this.setState.bind(this);

        var body;
        if (this.state.errorMsg) {
            return (
                <div className="chapter-container">
                    <Alert msg={this.state.errorMsg} />
                </div>
            );
        }

        return (
            <div className="container">
                <div className="poros">
                    <div className="tengah">
                        <div className="row">
                        { 
                            data.error ? <Alert msg={'There some image cannot be loaded for this chapter'} />: (
                            <span>
                                <h2 className="chapter-name">{name}</h2>

                                <ActionBar info={info}  setState={setState} />
                                <Loading loading={fetching} />
                            {pages}
                                <ActionBar info={info} setState={setState} />
                            </span>
                        )}
                        </div>
                    </div>
                </div>

            </div>
        );
    },

    componentDidMount: function () {
        var data = this.props.data.chapter;
        data.error ? this.setState({fetching: false}): this.fetchPages(data);
    },

    getInitialState: function () {
        return {
            info: {
                pages: [],
                name: '',
                series_url: '',
                next_chapter_url: null,
                prev_chapter_url: null
            },
            fetching: true,
            processingBookmark: false
        };
    },

    fetchPages: function (data) {
        var newState = this.state;
        newState.cards = [],
        newState.fetching = true;
        this.setState(newState);
        this.updateChapterData(data);
    },

    updateChapterData: function(data) {
        this.setState({
            info: data,
            fetching: false
        });
    }
});

var ActionBar = React.createClass({
    render: function () {
        var prevBtn = '';
        var nextBtn = '';
        var seriesBtn = '';

        var info = this.props.info;
        var prev = info.prev_chapter_url;
        var next = info.next_chapter_url;
        var series = info.series_url;

        if (prev !== null) {
            //prev = '/chapter/' + encodeURIComponent(prev);
            prevBtn = (
                <a href={prev} className="btn btn-primary" id="prev-btn">
                    <i className="fa fa-lg fa-angle-double-left fa-fw"></i> prev
                </a>
            );
        }

        if (next !== null) {
            //next = '/chapter/' + encodeURIComponent(next);
            nextBtn = (
                <a href={next} className="btn btn-primary" id="next-btn">
                    next
                    <i className="fa fa-lg fa-angle-double-right fa-fw"></i>
                </a>
            );
        }

        seriesBtn = (
            <Link to="series" params={{seriesSlug: series}} className="btn btn-info" id="chapter-list-btn">
                <i className="fa fa-lg fa-angle-double-up fa-fw"></i> chapter_list
            </Link>
        );

        return (
            <div className="chapter-navs  btn-group">
                {prevBtn} {seriesBtn} {nextBtn}
            </div>
        );
    }
});