# Mirador API Clients

While Mirador's RESTful realtime API takes the pain out of image moderation (no more queuing systems, webhooks, or custom integrations), nothing is easier than using a pre-implemented wrapper!

This repo contains implementations in a few languages, and even a couple of command-line cURL one-liners. See just how easy it is to integrate Mirador into your system. In all languages, results have the following fields:

* **`name`**: (string) the name of the file or the url requested
* **`safe`**: (boolean) if the image is "SFW" or "NSFW" (above or below our tuned threshold)
* **`value`**: (float, 0.0-1.0) the raw rating from the Mirador API; you can tune your own threshold

## Python
The mirador python wrapper uses the popular [requests](http://docs.python-requests.org/en/latest/) library.

```python

import mirador

mc = MiradorClient('your_key_here')

for result in mc.classify_files('bathing-suit.jpg', 'nsfw-user-upload.png'):
    print "image: {0}, safe: {1}, value: {2}".format(result.name, result.safe, result.value)

for result in mc.classify_urls('http://possibly-nsfw.com/cool.png', 'http://mysite.net/image/bad-picture.jpg'):
    print "image: {0}, safe: {1}, value: {2}".format(result.name, result.safe, result.value)

```

To get started, just do a simple: `pip install requests` and copy `mirador.py` into your project

## Ruby
Naturally our Ruby wrapper uses [httparty](http://johnnunemaker.com/httparty/), so if you don't have it, please `gem install httparty`

```ruby

require 'mirador'

mc = Mirador::Client.new('your_key_here')
mc.classify_files('bathing-suit.jpg', 'nsfw-user-upload.png').each do |result|
  puts "name: #{ result.name }, safe: #{ result.safe }, value: #{ result.value }"
end

mc.classify_urls('http://possibly-nsfw.com/cool.png', 'http://mysite.net/image/bad-picture.jpg').each do |result|
  puts "name: #{ result.name }, safe: #{ result.safe }, value: #{ result.value }"
end

```

## Node.js (Javascript)
For Node we're making use of [restler](https://github.com/danwrong/restler); right now you'll have to `npm install restler` but in the future we'll be packaging this together

```js

var mirador = require('mirador');
var mc = new mirador.MiradorClient('your_key_here');

mc.classifyFiles(['bathing-suit.jpg', 'nsfw-user-upload.png'], function (results, err) {

  results.forEach(function (result) {
    console.log('name: ' + result.name + ' safe: ' + result.safe + ' value: ' + result.value);
  });

});

mc.classifyUrls(['http://possibly-nsfw.com/cool.png', 'http://mysite.net/image/bad-picture.jpg'], function (results, err) {

  results.forEach(function (result) {
    console.log('name: ' + result.name + ' safe: ' + result.safe + ' value: ' + result.value);
  });

});

```
