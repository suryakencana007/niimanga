var React = require("react"),
    DropZone = require('components/dropzone/DropZone'),
    GenreSeries = require('pages/manga/genresfield');

module.exports = React.createClass({
     getInitialState: function () {
        return {
            files: [],
            genres: ''
        }
    },

    _onChangeGenres: function (v) {
        this.setState({genres: v});
    },

    _onDrop: function (file) {
        this.setState({
            files: file
        });
    },

    render: function() {
        return (
            <form className="form-horizontal">
                <div className="form-group">
                    <div className="row">
                        <label className="col-md-4 control-label" for="title">Type</label>
                        <div className="col-md-6">
                            <select id="type" name="type" className="form-control">
                                <option value="">---Type---</option>
                                <option value="kk">Scanlation</option>
                                <option value="sp">Self Published</option>
                                <option value="bt">Batoto</option>
                                <option value="ed">Mangaeden</option>
                            </select>
                            <span className="help-block"></span>
                        </div>
                    </div>
                    <div className="row">
                        <label className="col-md-4 control-label" for="title">Name</label>
                        <div className="col-md-6">
                            <input id="title" name="title" type="text" placeholder="Series Name" className="form-control input-md" />
                            <span className="help-block">Here goes your title series</span>
                        </div>
                    </div>
                    <div className="row">
                        <label className="col-md-4 control-label" for="aka">Alternative</label>
                        <div className="col-md-6">
                            <input id="aka" name="aka" type="text" placeholder="Alternative Name" className="form-control input-md" />
                            <span className="help-block">Here goes your Alt name</span>
                        </div>
                    </div>
                     <div className="row">
                        <label className="col-md-4 control-label" for="released">Released</label>
                        <div className="col-md-6">
                            <input id="released" name="released" type="text" placeholder="Released Years" className="form-control input-md" />
                            <span className="help-block">Here goes your Released Years</span>
                        </div>
                    </div>
                     <div className="row">
                        <label className="col-md-4 control-label" for="genres">Genres</label>
                        <div className="col-md-6">
                             <GenreSeries
                                name="genres"
                                value={this.state.genres}
                                onChange={this._onChangeGenres}
                            />
                            <span className="help-block">Here goes genres Series</span>
                        </div>
                    </div>

                    <div className="row">
                        <label className="col-md-4 control-label" for="description">Description</label>
                        <div className="col-md-6">
                            <textarea id="description" name="description" type="text" placeholder="description" className="form-control input-md"></textarea>
                            <span className="help-block">Here goes your description series</span>
                        </div>
                    </div>
                    <div className="row">
                        <label className="col-md-4 control-label" for="status">Status</label>
                        <div className="col-md-6">
                            <select id="status" name="status" className="form-control">
                                <option value="">---Status---</option>
                                <option value="1">Ongoing</option>
                                <option value="2">Completed</option>
                            </select>
                            <span className="help-block"></span>
                        </div>
                    </div>
                    <div className="row">
                        <label className="col-md-4 control-label" for="authors">Authors</label>
                        <div className="col-md-6">
                            <input id="authors" name="authors" type="text" placeholder="Authors Name" className="form-control input-md" />
                            <span className="help-block">Here goes your group name</span>
                        </div>
                    </div>
                    <div className="row">
                        <label className="col-md-4 control-label" for="artist">Artist</label>
                        <div className="col-md-6">
                            <input id="artist" name="artist" type="text" placeholder="Artist Name" className="form-control input-md" />
                            <span className="help-block">Here goes your artist name</span>
                        </div>
                    </div>
                    <div className="row">
                        <label className="col-md-4 control-label" for="category">Category</label>
                        <div className="col-md-6">
                            <select id="category" name="category" className="form-control">
                                <option value="">---category---</option>
                                <option value="ja">Manga (japanese)</option>
                                <option value="ko">Manhwa (korea)</option>
                                <option value="zh">Manhua (chinese)</option>
                                <option value="ot">Others</option>
                            </select>
                            <span className="help-block"></span>
                        </div>
                    </div>
                    <div className="row">
                        <label className="col-md-4 control-label" for="upload">Upload Cover</label>
                        <div className="col-md-6">
                            <DropZone ref="dropZone" multiple={false} onDrop={this._onDrop} urlXhr='/upload' methodXhr='POST' />
                            <span className="help-block">please *jpg image upload</span>
                        </div>
                    </div>
                </div>
            </form>
        );
    }
});