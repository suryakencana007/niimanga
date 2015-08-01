var React = require('react'),
    $ = require('jquery'),
    _ = require('lodash'),
    GridTable = require('components/Grid'),
    Modal = require('components/modal'),
    Form = require('pages/chapter/form');

module.exports = React.createClass({
    getInitialState:function () {
        return {
            lang: []
        };
    },

    componentDidMount: function () {
        var node = React.findDOMNode(this.refs.formChapter);
        this.$modal = $(node);
        $.get('cms/chapter/lang', function (result) {
            console.log(result);
            if (this.isMounted()) {
                var returns = [];
                result.rows.map(function(data, i){
                    returns.push({
                        value: data.value,
                        text: data.label
                    });
                });
                this.setState({
                    lang: returns
                });
            }
        }.bind(this));
    },

    _onClickBtnAdd: function () {
        this.refs.formChapter.show();
    },

    _onClickSave: function() {
        var form = this.$modal.find('form');
        var arrform = form.serializeArray();

        var data = {};
        _.map(arrform, function(arr, i){
            console.log(arr);
            data[arr.name] = arr.value;
        });
        //var uuid = form.find('[data-uuid]'),
        //    resUUID = [];
        var uuid = form.find('[data-uuid]').data('uuid');
        data['uuid'] = uuid;
        //_.map(uuid, function(item) {
        //    resUUID.push(item.data('uuid'));
        //});
        //console.log(resUUID);
        //data['uuid'] = this.refs.formChapter.getFileUUID();
        var self = this;
        $.post('/cms/chapter/save-new', data)
            .done(function( data ) {
                self.refs.tableChapter.refresh();
                self.refs.formChapter.close();
            });
        console.log('save on');
    },

    render: function() {
        return (
            <div>
                <div className="container">
                    <div className="row">
                        <div className="latest-list col-md-12">
                            <div className="title-green">Table Series</div>
                            <GridTable ref="tableChapter" handleAdd={this._onClickBtnAdd} btnadd="true" url="/cms/chapter/src" usave="/cms/chapter/edit-able" fields={
                                [
                                    { 'field': 'id', 'title': 'ID'},
                                    { 'field': 'mangaid', 'title': 'SeriesID', visible: false},
                                    { 'field': 'manga', 'title': 'Series'},
                                    { 'field': 'title', 'title': 'Chapter Title', 'editable': true},
                                    { 'field': 'volume', 'title': 'Volume', 'editable': true},
                                    { 'field': 'chapter', 'title': 'Chapter', 'editable': true},
                                    { 'field': 'lang', 'title': 'Language',
                                        'editable': {
                                            type: 'select',
                                            source: [
                                                {value: 'en', text: 'English'},
                                                {value: 'ja', text: 'Japanese'},
                                                {value: 'ko', text: 'Korean'},
                                                {value: 'zh', text: 'Chinese'},
                                                {value: 'fr', text: 'French'},
                                                {value: 'de', text: 'German'},
                                                {value: 'es', text: 'Spanish'},
                                                {value: 'it', text: 'Italian'}
                                            ]
                                        }
                                    },
                                    { 'field': 'slug', 'title': 'Slug Name' }
                                ]
                                }
                            />
                        </div>
                    </div>
                </div>
                <Modal ref="formChapter"
                    title="Chapter Form"
                    body={Form}
                    save={this._onClickSave}
                />
            </div>
        );
    }
});