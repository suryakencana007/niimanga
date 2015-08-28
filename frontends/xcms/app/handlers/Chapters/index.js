/** @flow */

import React, { Component, PropTypes, findDOMNode} from'react';
import _ from 'lodash';
import api from 'utils/api';
import cache from 'utils/cache';
import GridTable from 'components/GridTable';
import $ from 'jquery';


export default class Chapters extends Component {

    static fetchData = (token, params, query) => {
        return api.get('/chapter/end/lang', token).then(function(data){
            var results  = [];
            data.rows.map((item) => {
                results.push( {
                    value: item.value,
                    label: item.label
                });
            });
            return results;
        }).then(null , function(){
            return {error: true};
        });
    }

    constructor() {
        super();
        this.state = {
            lang: []
        };
    }

    componentDidMount() {}

    _onClickBtnAdd = () => {
        this.refs.formChapter.show();
    };

    _onClickSave = () => {
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
        $.post('/cms/chapter/save-new', data)
        .done(function( data ) {
            self.refs.tableChapter.refresh();
            self.refs.formChapter.close();
        });    
    };

    render(): any {
        let API = '/api/1.0';
        var data = this.props.data;
        console.log(data);
        return (
            <div>
            <div className="container">
            <div className="row">
            <div className="latest-list col-md-12">
            <div className="title-green">Table Series</div>
            <GridTable ref="tableChapter" handleAdd={this._onClickBtnAdd} btnadd="true" 
            url={API+"/chapter/end/src"} 
            usave={API+"/chapter/end/edit-able"}
            fields={
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

        </div>
        );
}
}