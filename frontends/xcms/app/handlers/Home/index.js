/** @flow */

import React, { Component, PropTypes } from 'react/addons';
import Button from 'components/base/Button';

export default class Home extends Component {
    constructor(props) {
        super(props);
        this._onClickBtn = this._onClickBtn.bind(this);
    }

    _onClickBtn() {
        let { MessageBox } = this.props;
        MessageBox('from home too', 'debug');
    }

    render(): any {
        console.log(this.props.errorMessage);
        return (
            <div>
                <div className="container">
                    <div className="row">
                        <div className="latest-list col-md-12">
                            <div className="title-green">Selamat Datang di CMS Niimanga</div>
                            <Button onClick={this._onClickBtn}>ok</Button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}