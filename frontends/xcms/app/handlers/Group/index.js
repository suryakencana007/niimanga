/** @flow */

import React, { Component, PropTypes} from'react';
import _ from 'lodash';
import api from 'utils/api';
import cache from 'utils/cache';
import GridTable from 'components/GridTable';

export default class Group extends Component {
    constructor() {
        super();
        this.state = {
            files: [],
            number: 0
        }
    }

    componentDidMount() {
      
    }

    _onClickBtnAdd = () => {
      
    };

    _onClickSave = () => {
        var arrform = this.$form.find('form').serializeArray();
        var data = {};
        _.map(arrform, function(arr, i){
            console.log(arr)
            data[arr.name] = arr.value;
        });
        var self = this;
        api.post('/cms/grp/save-new', data, this.props.token)
            .then(function( data ) {
                cache.expire(this.props.token, url);
                self.refs.tableGroup.refresh();
            });
        console.log('save on');
    };

    _onChange = () => {

    };

    render(): any {
        return (
            <div>
                <div className="container">
                    <div className="row">
                        <div className="latest-list col-md-12">
                            <div className="title-green">Table Groups</div>

                            <GridTable ref="tableGroup" 
                            handleAdd={this._onClickBtnAdd} 
                            btnadd="true" 

                            url="/cms/grp/src" fields={
                                [
                                    { 'field': 'id', 'title': 'ID'},
                                    { 'field': 'name', 'title': 'Group Name', 'editable': true},
                                    { 'field': 'slug', 'title': 'Slug Name', 'editable': true}
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