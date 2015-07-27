var React = require('react'),
    _ = require('lodash'),
    ajax = require('components/Ajax'),
    Loading = require('components/Loading'),
    Card = require('components/manga/Card'),
    cached = require('stores/cached');

var CardList = React.createClass({
    renderCard: function (card, index){
        return(
            <Card manga={card}/>
        );
    },

    render: function() {
        return(
            <div className="latest-list">
                <div className="title-green">Genre Manga</div>
                <Loading loading={this.props.fetching} />
            {this.props.manga.map(this.renderCard)}
            </div>
        );
    }
});

var search = React.createClass({
    contextTypes: {
        router: React.PropTypes.func.isRequired
    },

    componentWillReceiveProps: function (nextProps) {
        var query = nextProps.params.q;
        this.fetchCards(query);
    },

    componentDidMount: function (){
        var params = this.context.router.getCurrentParams();
        this.fetchCards(params.q);
    },

    getInitialState: function () {
        return {
            cards : [],
            fetching: true
        }
    },

    fetchCards: function (query) {
        var newState = this.state;
        newState.cards = [],
        newState.fetching = true;
        this.setState(newState);
        var cachedData = cached.get('genre_' + query);
        if (cachedData !== null) {
            this.updateCardsData(cachedData);
            //this.startProgressTimer();
            //console.log('cached');
            return;
        }

        var self = this;
        ajax.toAjax({
            url: '/api/v1/genre?q='+query,
            dataType: 'json',
            method: 'GET',
            success: function (data) {
                cached.set('genre_' + query, data);
                self.updateCardsData(data);
                //console.log(data);
            }.bind(self),
            error: function (data) {
                //self.setState({
                //    errorMsg: data.responseJSON.msg
                //});
                console.log(data);
            }.bind(self),
            complete: function () {
                self.setState({fetching: false});
            }.bind(self)
        });
    },

    updateCardsData: function (data) {
        this.setState({
            cards: data,
            fetching: false
        });
    },

    render: function() {
        return (
            <div>
                <div className="container">
                    <div className="row">
                        <CardList manga={this.state.cards} fetching={this.state.fetching} />
                    </div>
                </div>
            </div>
        );
    }
});

module.exports = search;