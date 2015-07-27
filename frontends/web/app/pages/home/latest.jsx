var React = require('react'),
    _ = require('lodash'),
    ajax = require('components/Ajax'),
    Loading = require('components/Loading'),
    Scroller = require('components/scroller/Scroller'),
    Card = require('components/manga/Card');

var CardList = React.createClass({
    _onRequestMoreItems: function (){
        console.log('scroller it!!!');
    },

    renderCard: function (card, index){
        return(
            <Card manga={card}/>
        );
    },

    render: function() {
        return(
            <div className="latest-list">
                <div className="title-green">Latest Manga Release</div>
                <Loading loading={this.props.fetching} />
                <Scroller
                hasMore={false}
                isScrollContainer={true}
                onRequestMoreItems={this._onRequestMoreItems}>
                {this.props.manga.map(this.renderCard)}
                </Scroller>
            </div>
        );
    }
});

var latest = React.createClass({
    componentDidMount: function (){
        this.fetchCards(this.props.url);
    },

    getInitialState: function () {
        return {
            cards : [],
            fetching: false
        }
    },

    fetchCards: function (url) {
        var newState = this.state;
        newState.cards = [];
        newState.fetching = true;

        this.setState(newState);

        var self = this;
        ajax.toAjax({
            url: '/api/v1/latest',
            dataType: 'json',
            method: 'POST',
            success: function (data) {
                //cached.set('chapter_' + url, data);
                self.updateCardsData(data);
                console.log(data);
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
            cards: data
        });
    },

    render: function() {
        return (<CardList manga={this.state.cards} fetching={this.state.fetching} />);
    }
});

module.exports = latest;