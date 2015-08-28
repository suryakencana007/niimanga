/** @flow */

import React, { Component, PropTypes, findDOMNode} from'react';
import _ from 'lodash';
import api from 'utils/api';
import cache from 'utils/cache';
import router from 'utils/router';

import GridTable from 'components/GridTable';
import $ from 'jquery';

    
export default class Series extends Component {
    constructor() {
        super();
        this._onClickEdit = this._onClickEdit.bind(this);
        this._onClickRemove = this._onClickRemove.bind(this);
    }

    componentDidMount() {}

    _onClickEdit(row, index){
        router.transitionTo('series_edit', {seriesSlug: row.slug});
        console.log(row, index);
    }

    _onClickRemove(row, index){
        console.log(row, index);
    }

    render(): any {
        let API = '/api/1.0';
        return (
            <div>
                <div className="container">
                    <div className="row">
                        <div className="latest-list col-md-12">
                            <div className="title-green">Table Series</div>
                            <GridTable ref="tableSeries" btnadd="true" 
                            onClickEdit={this._onClickEdit} onClickRemove={this._onClickRemove}
                            url={API+"/series/end/src"} fields={
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
            </div>
        );
    }
}