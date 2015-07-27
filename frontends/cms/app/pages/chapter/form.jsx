var React = require("react"),
    DropZone = require('components/dropzone/DropZone'),
    SelectSeries = require('pages/chapter/seriesfield'),
    SelectLang = require('pages/chapter/langfield');

module.exports = React.createClass({

    getInitialState: function () {
        return {
            files: [],
            series: '',
            lang: ''
        }
    },

    _onChangeSeries:function(v) {
        this.setState({series: v});
    },

    _onChangeLang:function(v) {
        this.setState({lang: v});
    },

    _onDrop: function (file) {
        this.setState({
            files: file
        });
    },

    getFileUUID: function() {
      return this.refs.dropZone.getFileUUID();
    },

    render: function() {
        return (
            <form className="form-horizontal">
                <div className="form-group">
                    <div className="row">
                        <label className="col-md-4 control-label" for="manga">Series</label>
                        <div className="col-md-6">
                            <SelectSeries
                                name="series"
                                value={this.state.series}
                                searchable={true}
                                onChange={this._onChangeSeries}
                            />
                            <span className="help-block"></span>
                        </div>
                    </div>
                    <div className="row">
                        <label className="col-md-4 control-label" for="title">Chapter Title</label>
                        <div className="col-md-6">
                            <input id="title" name="title" type="text" placeholder="Chapter Title" className="form-control input-md" />
                            <span className="help-block">Here goes your Chapter Title</span>
                        </div>
                    </div>
                    <div className="row">
                        <label className="col-md-4 control-label" for="lang">Language</label>
                        <div className="col-md-6">
                            <SelectLang
                                name="lang"
                                value={this.state.lang}
                                searchable={true}
                                onChange={this._onChangeLang}/>
                                <span className="help-block"></span>
                        </div>
                    </div>
                     <div className="row">
                        <label className="col-md-4 control-label" for="chapter">Chapter</label>
                        <div className="col-md-6">
                            <input id="chapter" name="chapter" type="text" placeholder="Chapter no" className="form-control input-md" />
                            <span className="help-block">Here goes your Chapter no</span>
                        </div>
                    </div>
                    <div className="row">
                        <label className="col-md-4 control-label" for="volume">Volume</label>
                        <div className="col-md-6">
                            <input id="volume" name="volume" type="text" placeholder="Volume no" className="form-control input-md" />
                            <span className="help-block">Here goes your Volume no</span>
                        </div>
                    </div>
                    <div className="row">
                        <label className="col-md-4 control-label" for="upload">Upload Chapter</label>
                        <div className="col-md-6">
                            <DropZone ref="dropZone" multiple={false} onDrop={this._onDrop} urlXhr='/upload' methodXhr='POST' />
                            <span className="help-block">please *zip or rar upload</span>
                        </div>
                    </div>
                </div>
            </form>
        );
    }
});