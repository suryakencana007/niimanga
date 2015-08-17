import React from "react";
import {Component, PropTypes} from "react/addons";
import Select from'components/selectfield/Select';
import api from 'utils/api';

class SeriesField extends Component {
    static propTypes = {
        searchable: PropTypes.bool,
        onChange: PropTypes.func,
        name: PropTypes.string,
        value: PropTypes.object
    };

    static defaultProps = {
        searchable: false,
        name: "",
        value: null
    };   

    _onChange = (newValue) => {
        this.props.onChange && this.props.onChange(newValue);
    };

    render(): any {
        return (
            <Select
                asyncOptions={this.fetchSeries}
                name={this.props.name}
                ref="selectSeries"
                
                value={this.props.value}
                onChange={this._onChange} />
        );
    };

    fetchSeries = (input, callback) => {
        input = input.toLowerCase();
        if(input.length > 1) {
            var url = '/series/end/search?q=' + input;
            var result = api.post(url, this.props.token).then((data) => {
                cache.expire(this.props.token, url);
                var opts = {}
                if (data.rows.length > 0) {
                    opts = {
                        options: data.rows,
                        complete: true
                    };
                    console.log('search');
                } else {
                    opts.complete = false;
                }
                callback(null, opts);
                return;
            });
        }
        callback(null, {complete: false});
    };
}

module.exports = SeriesField;