/**
 * Taken, CommonJS-ified, and heavily modified from:
 * https://github.com/flyingsparx/NodeDirectUploader
 */

BasicUpload.prototype.url = '/sign-Basic';
BasicUpload.prototype.files = null;

BasicUpload.prototype.onFinishBasicPut = function(signResult) {
    return console.log('base.onFinishBasicPut()', signResult);
};

BasicUpload.prototype.onProgress = function(percent, status) {
    return console.log('base.onProgress()', percent, status);
};

BasicUpload.prototype.onError = function(status) {
    return console.log('base.onError()', status);
};

function BasicUpload(options) {
    if (options == null) {
        options = {};
    }
    for (option in options) {
        if (options.hasOwnProperty(option)) {
            this[option] = options[option];
        }
    }
    this.handleFileSelect(this.methodXhr, this.files);
}

BasicUpload.prototype.handleFileSelect = function(method, files) {
    this.onProgress(0, 'Upload started.');
    var files = files;
    var result = [];
    for (var i=0; i < files.length; i++) {
        var f = files[i];
        result.push(this.uploadFile(method, f));
    }
    return result;
};

BasicUpload.prototype.createCORSRequest = function(method, url) {
    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType && xhr.overrideMimeType('text/plain; charset=x-user-defined');
    if (xhr.withCredentials != null) {
        xhr.open(method, url, true);
    }
    else if (typeof XDomainRequest !== "undefined") {
        xhr = new XDomainRequest();
        xhr.open(method, url);
    }
    else {
        xhr = null;
    }
    return xhr;
};

BasicUpload.prototype.executeOnSignedUrl = function(file, callback) {
    var xhr = new XMLHttpRequest();
    var fileName = file.name.replace(/\s+/g, "_");
    xhr.open('GET', this.url + '?objectName=' + fileName + '&contentType=' + file.type, true);
    xhr.overrideMimeType && xhr.overrideMimeType('text/plain; charset=x-user-defined');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var result;
            try {
                result = JSON.parse(xhr.responseText);
            } catch (error) {
                this.onError('Invalid signing server response JSON: ' + xhr.responseText);
                return false;
            }
            return callback(result);
        } else if (xhr.readyState === 4 && xhr.status !== 200) {
            return this.onError('Could not contact request signing server. Status = ' + xhr.status);
        }
    }.bind(this);
    return xhr.send();
};

BasicUpload.prototype.uploadToS3 = function(file, signResult) {
    var xhr = this.createCORSRequest('PUT', signResult.signedUrl);
    if (!xhr) {
        this.onError('CORS not supported');
    } else {
        xhr.onload = function() {
            if (xhr.status === 200) {
                this.onProgress(100, 'Upload completed.');
                return this.onFinishBasicPut(signResult);
            } else {
                return this.onError('Upload error: ' + xhr.status);
            }
        }.bind(this);
        xhr.onerror = function() {
            return this.onError('XHR error.');
        }.bind(this);
        xhr.upload.onprogress = function(e) {
            var percentLoaded;
            if (e.lengthComputable) {
                percentLoaded = Math.round((e.loaded / e.total) * 100);
                return this.onProgress(percentLoaded, percentLoaded === 100 ? 'Finalizing.' : 'Uploading.');
            }
        }.bind(this);
    }
    xhr.setRequestHeader('Content-Type', file.type);
    xhr.setRequestHeader('x-amz-acl', 'public-read');
    return xhr.send(file);
};

BasicUpload.prototype.uploadToBasic = function(method, file) {
    var formData = new FormData();
    formData.append('dropfile', file);
    var xhr = this.createCORSRequest(method, this.urlXhr);
    if (!xhr) {
        this.onError('CORS not supported');
    } else {
        xhr.onload = function() {
            if (xhr.status === 200) {
                this.onProgress(100, 'Upload completed.');
                return this.onFinishBasicPut(xhr.responseText);
            } else {
                return this.onError('Upload error: ' + xhr.status);
            }
        }.bind(this);
        xhr.onerror = function() {
            return this.onError('XHR error.');
        }.bind(this);
        xhr.upload.onprogress = function(e) {
            var percentLoaded;
            if (e.lengthComputable) {
                percentLoaded = Math.round((e.loaded / e.total) * 100);
                return this.onProgress(percentLoaded, percentLoaded === 100 ? 'Finalizing.' : 'Uploading.');
            }
        }.bind(this);
    }
    console.log(file);
    xhr.setRequestHeader('Content-Type', file.type);
    console.log('uploadToBasic');
    return xhr.send(formData);
};

BasicUpload.prototype.uploadFile = function(method, file) {
    return this.uploadToBasic(method, file);
};

//BasicUpload.prototype.uploadFile = function(file) {
//    return this.executeOnSignedUrl(file, function(signResult) {
//        return this.uploadToBasic(file, signResult);
//    }.bind(this));
//};


module.exports = BasicUpload;