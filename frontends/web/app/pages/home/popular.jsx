var React = require('react');
var _ = require('lodash');
var Radium = require('radium');
var cache = require('utils/cache');
var api = require('utils/api');
var Loading = require('components/Loading');
var Scroller = require('components/scroller/Scroller');
var ListCard = require('components/manga/ListCard');

var popular = React.createClass({
    getInitialState: function () {
        return {
            limit: 8,
            offset: 0,
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
        var url = '/api/v1/popular?page=' + newState.offset + '&cards=' + newState.limit;
        var result = api.post(url, this.props.token).then((data) => {
           cache.expire(this.props.token, url);
           self.updateCardsData(data);
           self.setState({fetching: false});
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
            <span>
                <div className="popular-list" style={styles.wrapperList}>
                    <div className="title-green">Popular Manga</div>
                    <Scroller
                    hasMore={true}
                    isScrollContainer={true}
                    onRequestMoreItems={this._onRequestMoreItems}
                    style={styles.messagesList}>
                    {this.state.cards.map(this.renderCard)}
                    </Scroller>
                </div>
                <Loading loading={this.state.fetching} />
            </span>
            );
    }
});

var styles = {
    wrapperList: {
        height: '520px',
        overflow: 'hidden'
    },
    messagesList: {
        height: '100%'
    },
}
module.exports = popular;