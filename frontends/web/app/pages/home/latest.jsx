var React = require('react'),
_ = require('lodash'),
Radium = require('radium'),
ajax = require('components/Ajax'),
Loading = require('components/Loading'),
Scroller = require('components/scroller/Scroller'),
Card = require('components/manga/Card');

var latest = React.createClass({
    getInitialState: function () {
        return {
            limit: 16,
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
            url: '/api/v1/latest?page=' + newState.offset + '&cards=' + newState.limit,
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
        return <Card manga={card} key={index}/>;
    },

    render: function() {
        return(
            <span>
                <div className="latest-list" style={styles.wrapperList}>
                    <div className="title-green">Latest Manga Release</div>
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
        height: '1058px',
        overflow: 'hidden'
    },
    messagesList: {
        height: '100%'
    },
}
module.exports = latest;