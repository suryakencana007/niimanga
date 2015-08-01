var React = require('react'),
    $ = require('jquery'),
    _ = require('lodash'),
    GridTable = require('components/Grid'),
    Modal = require('components/modal'),
    Form = require('pages/manga/form');

module.exports = React.createClass({
    componentDidMount: function () {
        var node = React.findDOMNode(this.refs.formSeries);
        this.$modal = $(node);
    },

    _onClickBtnAdd: function () {
        this.refs.formSeries.show();
    },

    _onClickSave: function() {
        var form = this.$modal.find('form');
        var arrform = form.serializeArray();
        var data = {};
        _.map(arrform, function(arr, i){
            console.log(arr);
            data[arr.name] = arr.value;
        });
        var uuid = form.find('[data-uuid]').data('uuid');
        data['uuid'] = uuid;
        var self = this;
        $.post('/cms/series/save-new', data)
            .done(function( data ) {
                self.refs.tableSeries.refresh();
                self.refs.formSeries.close();
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
                            <GridTable ref="tableSeries" handleAdd={this._onClickBtnAdd} btnadd="true" url="/cms/series/src" usave="/cms/series/edit-able" fields={
                                [
                                    { 'field': 'id', 'title': 'ID'},
                                    { 'field': 'title', 'title': 'Name', 'editable': true},
                                    { 'field': 'authors', 'title': 'Author', 'editable': true},
                                    { 'field': 'artist', 'title': 'Artist', 'editable': true},
                                    { 'field': 'description', 'title': 'Description',
                                        'editable': {
                                            type: 'textarea'
                                        }
                                    },
                                    { 'field': 'category', 'title': 'Category',
                                        editable: {
                                            type: 'select',
                                            source: [
                                                {value: 'ja', text: 'Manga (Japanese)'},
                                                {value: 'ko', text: 'Manhwa (Korean)'},
                                                {value: 'zh', text: 'Manhua (Chinese)'}
                                            ]
                                        }
                                    },
                                    { 'field': 'released', 'title': 'Released', 'editable': true},
                                    { 'field': 'status', 'title': 'Status',
                                        editable: {
                                            type: 'select',
                                            source: [
                                                {value: '1', text: 'Ongoing'},
                                                {value: '2', text: 'Completed'}
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
                <Modal ref="formSeries"
                    title="Series Form"
                    body={Form}
                    save={this._onClickSave}
                />
            </div>
        );
    }
});