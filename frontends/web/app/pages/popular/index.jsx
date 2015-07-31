var React = require('react'),
_ = require('lodash'),
Radium = require('radium'),
ajax = require('components/Ajax'),
Loading = require('components/Loading'),
InfiniteScroll = require('components/scroller/InfiniteScroll'),
ListCard = require('components/manga/ListCard');

var popular = React.createClass({
    getInitialState: function () {
        return {
            limit: 25,
            offset: 1,
            cards : [],
            fetching: false
        }
    },

    fetchCards: function () {
        var newState = this.state;
        // newState.cards = [];
        newState.fetching = true;

        this.setState(newState);

        var self = this;
        ajax.toAjax({
            url: '/api/v1/popular?page=' + newState.offset + '&cards=' + newState.limit,
            dataType: 'json',
            method: 'POST',
            success: function (data) {
                //cached.set('chapter_' + url, data);
                self.updateCardsData(data);
                // console.log(data);
            }.bind(self),
            error: function (data) {

            }.bind(self),
            complete: function () {
                self.setState({fetching: false});
            }.bind(self)
        });
    },

    updateCardsData: function (data) {
        this.setState({
            cards: this.state.cards.concat(data),
            offset: this.state.offset + 1
        });
    },

    _onRequestMoreItems: function (){
        this.fetchCards();
    },
    
    renderCard: function (card, index){
        return <ListCard manga={card} key={index}/>;
    },

    render: function() {
        return(
           <div className="container">
           <div className="row">
                <div className="popular-list">
                    <div className="title-green">Popular Manga</div>
                    <InfiniteScroll
                    hasMore={true}
                    onRequestMoreItems={this._onRequestMoreItems}
                    threshold={250}
                    style={styles.messagesList}>
                    {this.state.cards.map(this.renderCard)}
                    </InfiniteScroll>
                </div>
                <Loading loading={this.state.fetching} />
            </div>
            </div>
            );
    }
});

var styles = {
    wrapperList: {
        height: '250px',
        overflow: 'hidden'
    },
    messagesList: {
        height: '100%'
    },
}
module.exports = popular;