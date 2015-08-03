var React = require('react');
var _ = require('lodash');
var UUID = require('utils/uuid');
var DzPreview = require('components/dropzone/DzPreview');
var BasicUpload = require('components/dropzone/xhr');

var Dropzone = React.createClass({
    getDefaultProps: function() {
        return {
            supportClick: true,
            multiple: true
        };
    },

    onProgress: function(percent, message, index) {
        var files = _.extend([], this.state.files);
        files[index].percent = percent;
        this.setState({files: files});
        console.log('Upload progress: ' + percent + '% ' + message);
    },
    onFinish: function(signResult) {
        console.log("Upload finished: " + signResult)
    },
    onError: function(message) {
        console.log("Upload error: " + message);
    },

    getInitialState: function() {
        return {
            isDragActive: false,
            files: [],
            uuid: []
        };
    },

    getFileUUID: function() {
        return this.state.uuid;
    },

    propTypes: {
        onDrop: React.PropTypes.func.isRequired,
        size: React.PropTypes.number,
        style: React.PropTypes.object,
        supportClick: React.PropTypes.bool,
        accept: React.PropTypes.string,
        multiple: React.PropTypes.bool
    },

    onDragLeave: function(e) {
        this.setState({
            isDragActive: false
        });
    },

    onDragOver: function(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
        this.setState({
            isDragActive: true
        });
    },

    onDrop: function(e) {
        e.preventDefault();

        this.setState({
            isDragActive: false
        });

        var files,
            fstate = this.state.files;
        if (e.dataTransfer) {
            files = e.dataTransfer.files;
        } else if (e.target) {
            files = e.target.files;
        }

        var maxFiles = (this.props.multiple) ? files.length : 1;
        if(this.props.multiple || fstate.length < 1) {
            for (var i = 0; i < maxFiles; i++) {
                files[i].preview = URL.createObjectURL(files[i]);
                files[i].precent = 0;
                files[i].uuid = UUID.generate();
                //proses upload
                var lenState = fstate.length > 0 ? fstate.length : 0;
                this._upload(files[i], i + lenState);
            }
            files = Array.prototype.slice.call(files, 0, maxFiles);
            this._addFile(files);
        }

        if (this.props.onDrop) {
            this.props.onDrop(fstate, e);
        }

    },

    _upload: function (files, index) {
        var self = this;
        var fd = new FormData();
        fd.append("DROPZONE", files);
        fd.append("uuid", files.uuid);
        var xhr = new XMLHttpRequest();
        xhr.overrideMimeType && xhr.overrideMimeType('text/plain; charset=x-user-defined');
        xhr.open(this.props.methodXhr, this.props.urlXhr, true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                self.onProgress(100, 'Upload completed.', index);
                return self.onFinish(xhr.responseText);
            } else {
                return self.onError('Upload error: ' + xhr.status);
            }
        }.bind(this);
        xhr.upload.onprogress = function(e) {
            var percentLoaded;
            if (e.lengthComputable) {
                percentLoaded = Math.round((e.loaded / e.total) * 100);
                return self.onProgress(percentLoaded, percentLoaded === 100 ? 'Finalizing.' : 'Uploading.', index);
            }
        }.bind(this);
        xhr.send(fd);

    },

    _addFile: function (file) {
        if (file) {
            var files = this.state.files,
                uuid = this.state.uuid;
            if (!files) {
                files = [];
                uuid = [];
            }
            _.map(file, function(item){
                files.push(item);
                uuid.push(item.uuid);
            });
            this.setState({
                files: files,
                uuid: uuid
            });
        }
    },

    onClick: function () {
        if (this.props.supportClick === true) {
            this.open();
        }
    },

    open: function() {
        var fileInput = React.findDOMNode(this.refs.fileInput);
        fileInput.value = null;
        fileInput.click();
    },

    previews: function() {
        var files = this.state.files;
        return Object.keys(files).map(function(uid) {
            return <DzPreview file={files[uid]} key={uid} />;
        });
    },

    render: function() {
        var previews = this.previews();
        var className = this.props.className || 'dropzone';
        if (this.state.isDragActive) {
            className += ' active';
        }

        var style = this.props.style || {
                minWidth: this.props.size || 100,
                minHeight: this.props.size || 100,
                borderStyle: this.state.isDragActive ? 'solid' : 'dashed'
            };

        return (
            <div className={className} style={style} onClick={this.onClick} onDragLeave={this.onDragLeave} onDragOver={this.onDragOver} onDrop={this.onDrop} >
                <input style={{display: 'none'}} type='file' multiple={ this.props.multiple } ref='fileInput' onChange={this.onDrop} accept={this.props.accept} />
            {previews}
            {this.props.children}
            </div>
        );
    }

});

module.exports = Dropzone;