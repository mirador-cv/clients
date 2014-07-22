var rest = require('restler');
var fs = require('fs');

function MiradorResult(name, data) {
  this.name = name;
  this.safe = data.safe;
  this.value = data.value;
}

function parseResult(names, results) {
  if (!results || !results.length) return [];


  return results.map(function (r, i) {
    return new MiradorResult(names[i], r.result);
  });

}

function resultHandler(names, done) {

  return function (data) {
    if (data.errors) {
      done(null, data.errors);
    }
    else {
      done(parseResult(names, data.results));
    }
  }
}


var Mirador = rest.service(function (apikey) {
  this.defaults.api_key = apikey;
}, {
  baseURL: 'http://api.mirador.im'
}, {

  classifyUrls: function (urls, done) {
    urls = typeof urls == 'string' ? [urls] : urls;

    var req = this.get(
      '/v1/classify', {query: { url: urls, api_key: this.defaults.api_key }}
    );

    req.on('complete', resultHandler(urls, done));

    req.on('error', function(err) {
      done(null, err);
    });

  },

  _classifyBase: function (files, images, done) {

    var req = this.post(
      '/v1/classify',
      {
        data: {
          api_key: this.defaults.api_key,
          image: images
        }
      });

    req.on('complete', resultHandler(files, done));
    req.on('error', function (err) {
      done(null, err);
    });

  },

  classifyFiles: function (files, done) {
    files = typeof files == 'string' ? [files] : files;


    // read files & convert to base64
    var processed = files.map(function (f) {
      return fs.readFileSync(f).toString('base64').replace('\n', '');
    });


    this._classifyBase(files, processed, done);
  },

  classifyRaw: function (buffers, done) {
    var k, processed = [], names = [];

    for(k in buffers) {
      (function(name, buffer) {

        names.push(name);
        processed.push(
          buffer.toString('base64').replace("\n", '')
        );

      }(k, buffers[k]));
    }


    this._classifyBase(names, process, done);
  },

});

module.exports = {
  MiradorClient: Mirador
};


var main = function () {

  var mirador = new Mirador('your_api_key');

  var result = mirador.classifyFiles(process.argv.slice(2), function (res, err) {

    if (!err) {
      console.log(res);
    }
    else {
      console.error(err);
    }

  });

}

if (require.main === module) main();
