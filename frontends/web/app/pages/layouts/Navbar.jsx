var React = require('react');
var Router = require('react-router');
var { Route, DefaultRoute, RouteHandler, Link } = Router;
var SearchBox = require('components/SearchBox');

var isMobile = require('utils/ismobile');

module.exports = React.createClass({
    mixins: [
        require('react-router').Navigation, // needed for transitionto
    ],

    getInitialState: function() {
        return {
            query: '',
            ismobile: false
        };
    },

    getDefaultProps: function() {
        return {
            genres: []
        }
    },

    componentWillMount: function() {
        this.setState({ismobile: isMobile()});
    },

    handleSearch: function (query) {
     /*   console.log(this.state.query);
        var query = this.state.query*/
        if (!query || query.trim().length < 2) {
            return;
        }
        this.transitionTo('search', {q: query});
        this.setState({query: ''});
    },

    handleChange: function(query) {
        // var val = event.target.value;
        // console.log(val);
        this.setState({query: query});
    },

    getGenres: function(gen, start, end) {
        gen = gen.slice(start, end);
        return Object.keys(gen).map(function(uid) {
            return (<li><Link to="genre" params={{q: gen[uid].value}}><i className="fa fa-folder-o fa-fw"></i><span className="title">{gen[uid].label}</span></Link></li>);
        });
    },

    render: function () {
        if(this.props.genres && this.props.genres.length > 0) {
            var genres_o = this.getGenres(this.props.genres, 0, 10);
            var genres_t = this.getGenres(this.props.genres, 10, 20);
            var genres_th = this.getGenres(this.props.genres, 20, 30);
            var genres_fo = this.getGenres(this.props.genres, 30, 40);
        }
        var navbar = (this.state.ismobile? 'navbar': 'navbar navbar-fixed-top');

        return (
            <header className={navbar} style={{borderWidth:' 0 0 1px', marginBottom: '0'}}>
                <div className="navbar-inner">
                    <div className="container clearfix">
                    { !this.state.ismobile? ( <span>
                        <div className="nav-logo">
                            <Link to="/" >Niimanga<span className="site-logo"></span></Link>
                        </div>
                        
                        <ul className="top-right-nav">
                            <li className="dropdown border-both">
                                <a data-toggle="dropdown" data-hover="dropdown" className="dropdown-toggle" href="#">Genres</a>
                                <div className="dropdown-menu">
                                    <div className="holder-dropdown-menu dropdown-category-thumb">
                                        <div className="row">
                                            <div className="col-md-3">
                                                <ul>
                                                {genres_o}
                                                </ul>
                                            </div>
                                            <div className="col-md-3">
                                                <ul>
                                                {genres_t}
                                                </ul>
                                            </div>
                                            <div className="col-md-3">
                                                <ul>
                                                {genres_th}
                                                </ul>
                                            </div>
                                            <div className="col-md-3">
                                                <ul>
                                                {genres_fo}
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        </ul>
                        <div className="pull-right">
                            <ul className="top-right-nav">
                                <li className="border-left">
                                    <Link to="latest" >Latest Manga</Link>
                                </li>
                                <li className="border-both">
                                    <Link to="popular" >Hot Manga</Link>
                                </li>
                            </ul>
                        </div>
                        </span>): (this.props.menuBar) }
                        <SearchBox
                        onQueryChange={this.handleChange}
                        onQuerySubmit={this.handleSearch}
                        query={this.state.query}
                        placeholder="Searching series name..."
                        />
                    </div>
                </div>
            </header>
        );
    }
});