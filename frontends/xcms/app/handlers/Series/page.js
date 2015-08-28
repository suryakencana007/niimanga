/** @flow */

import React, { Component, PropTypes, findDOMNode} from'react';
import _ from 'lodash';
import api from 'utils/api';
import { Link } from 'react-router';

import Button from 'components/base/Button';
import Input from 'components/base/Input';
import LabelEdit from 'components/LabelEdit';
import LoadingUI from 'components/LoadingUI';


class Chapter_list extends Component {
    constructor() {
        super();
        this.renderItem = this.renderItem.bind(this);
    }

    renderItem() {
        let chapters = _.map(this.props.chapters, function(chapter){
            let href = chapter.url.split('/');
            return (
                <Link to="chapter" params={{seriesSlug: href[0], chapterSlug: href[1]}} className="list-group-item">
                <span>{chapter.name}</span><span className="pull-right">{chapter.time}</span>
                </Link>
                )
        });
        return chapters;
    }

    render(): any {
        return (
            <div className="col-xs-12 list-group">
            {this.renderItem()}
            </div>
            );
    }
}

class Pages extends Component {

    static propTypes = {
        series: {
            "aka": PropTypes.string,
            "authors": PropTypes.array,
            "thumb_url": PropTypes.object,
            "name": PropTypes.string,
            "status": PropTypes.string,
            "description": PropTypes.array,
            "tags": PropTypes.array,
            "site": PropTypes.object,
            "time": PropTypes.object,
            "chapters": PropTypes.array
        },
        fetching: PropTypes.bool
    };

    static defaultProps ={
        series: {
            "aka": "",
            "authors": [],
            "thumb_url": null,
            "name": "",
            "status": "",
            "description": [],
            "tags": [],
            "site": null,
            "time": null,
            "chapters": []
        },
        fetching: true
    };

    constructor(props) {
        super(props);
        this._renderTags = this._renderTags.bind(this);
        let data = this.props.data.series_edit;
        this.state = {
           name: data.name
        };
    }

    _renderTags(tags){
        return tags.map(function(item){
            return (<div className="ticket"><Link to="genre" params={{q: item.value}}><i className="fa fa-tag fa-lg fa-fw"></i>{item.label}</Link></div>);
        });
    }

    _labelText(text) {
        this.setState({name: text});
    }

    render(): any {
        let series = this.props.data.series_edit
        let body;
       
        let href = series.last_url.split('/');
        body = (
            <div className="card books page left-cover">
                <div className="card-content">
                    <div className="col-md-2 col-xs-12 cover">
                        <div className="cover-image-container">
                            <div className="cover-outer-align">
                                <div className="cover-inner-align"><img className="cover-image" src={series.thumb_url}/></div>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-10 col-xs-12 detail">
                        <label className="title">{this.state.name}</label>
                        <LabelEdit saveText={this._labelText.bind(this)} text={this.state.name}><label className="title">{this.state.name}</label></LabelEdit>

                        <div className="col-xs-12 subtitle-container"><label className="subtitle" >{series.authors}</label></div>
                        <div className="col-xs-12 alias">{series.aka}</div>
                        <div className="col-xs-12 genres poros"><div className="tengah">{this._renderTags(series.tags)}</div></div>
                        <div className="col-xs-12 source-link">{series.origin}</div>
                       
                        <div className="col-xs-12 description"><p>{series.description}</p></div>
                    </div>
                </div>
            <div className="title-green" > Chapters <span className="pull-right" style={{padding:'5px'}}><Button><i className="fa fa-plus fa-fw"></i></Button></span></div>
            
            <Chapter_list chapters={series.chapters}/>
            </div>
            );
        
        return (
            <div className="row">
            {body}
            </div>
            );
    }
}

export default class SeriesPage extends Component {
    static fetchData(token, params, query) {
        let url = '/series/' + params.seriesSlug;
        return api.post(url, token).then(null ,
            function(){
                return {error: true};
            });
    };

    constructor(props) {
        super(props);
    }

    render(): any {
        return (
            <div>
            <div className="container">
           
            <Pages {...this.props}/>
            </div>
            </div>
           );
    }
}