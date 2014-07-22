# Mirador API Clients

While Mirador's RESTful realtime API takes the pain out of image moderation (no more queuing systems, webhooks, or custom integrations), nothing is easier than using a pre-implemented wrapper!

This repo contains implementations in a few languages, and even a couple of command-line cURL one-liners. See just how easy it is to integrate Mirador into your system. In all languages, results have the following fields:

* **`name`**: (string) the name of the file or the url requested
* **`safe`**: (boolean) if the image is "SFW" or "NSFW" (above or below our tuned threshold)
* **`value`**: (float, 0.0-1.0) the raw rating from the Mirador API; you can tune your own threshold

## Python
For the python library, please go to [github.com/mirador-cv/mirador-py](http://github.com/mirador-cv/mirador-py)

```bash
pip install mirador
```

## Ruby
For the ruby library, please go to [github.com/mirador-cv/mirador-rb](http://github.com/mirador-cv/mirador-rb)

```bash
gem install mirador
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

[node.js examples](mirador.js)


## PHP
We don't currently have a client for PHP, altho it's actually super easy to get started:

(using composer and [GuzzleHttp](http://docs.guzzlephp.org)):

```php

// one image/url with id attached
$req = $client->createRequest('POST', 'http://api.mirador.im/v1/classify', [
  'body' => [
    'api_key' => 'your_api_key',
    'url' => [
      'id' => 'nsfw',
      'data' => 'http://demo.mirador.im/test/nsfw.jpg'
    ]

  ]
]);

```
[php examples](Mirador.php)
