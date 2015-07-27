var React = require('react'),
    _ = require('lodash'),
    ajax = require('components/Ajax'),
    Loading = require('components/Loading'),
    ListCard = require('components/manga/ListCard');

var CardList = React.createClass({
    renderCard: function (card, index){
        return(
            <ListCard manga={card}/>
        );
    },

    render: function() {
        return(
            <div className="latest-list">
                <div className="title-green">Popular Manga</div>
                <Loading loading={this.props.fetching} />
            {this.props.manga.map(this.renderCard)}
            </div>
        );
    }
});

var popular = React.createClass({
    componentWillMount: function () {
        this.fetchCards();
    },

    componentDidMount: function (){
        //this.fetchCards();
    },

    getInitialState: function () {
        return {
            cards : [],
            fetching: false
        }
    },

    fetchCards: function () {
        var newState = this.state;
        newState.cards = [];
        newState.fetching = true;

        this.setState(newState);

        var self = this;
        ajax.toAjax({
            url: '/api/v1/popular',
            dataType: 'json',
            method: 'POST',
            success: function (data) {
                //cached.set('chapter_' + url, data);
                self.updateCardsData(data);
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

module.exports = popular;