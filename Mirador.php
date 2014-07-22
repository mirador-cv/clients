<?php
// (for composer)
require 'vendor/autoload.php';

// we'll use Guzzle
// http://docs.guzzlephp.org/en/latest/index.html
$client = new GuzzleHttp\Client();

// simple formatting for making a request
// since it's a url you're sending, no need to attach id/name metadata
$req = $client->createRequest('POST', "http://api.mirador.im/v1/classify", [
  'body' => [
    'api_key' => 'your_api_key',
    'url' => ['http://demo.mirador.im/test/nsfw.jpg', 'http://demo.mirador.im/test/baby.jpg'],
  ]
]);

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


// $res = $client->send($req);
// var_dump($res->json());

// attach an ids to each url/image
// we can do this with a URL to make it easier to join on index in a DB
$req = $client->createRequest('POST', 'http://api.mirador.im/v1/classify', [
  'body' => [
    'api_key' => 'your_api_key',
    'url' => [
      [
        'id' => 'nsfw',
        'data' => 'http://demo.mirador.im/test/nsfw.jpg',
      ],
      [
        'id' => 'baby',
        'data' => 'http://demo.mirador.im/test/baby.jpg'
      ]
    ]

  ]
]);

// $res = $client->send($req);
// var_dump($res->json());


// file upload example; php makes it easy!
$req = $client->createRequest('POST', 'http://api.mirador.im/v1/classify', [
  'body' => [
    'api_key' => 'your_api_key',
    'image' => [
      [
        'id' => 'porn2.jpg',
        'data' => base64_encode(file_get_contents('images/porn2.jpg')),
      ],
      [
        'id' => 'BrV7x8ICQAEH6Wi.jpg',
        'data' => base64_encode(file_get_contents('images/BrV7x8ICQAEH6Wi.jpg'))
      ]
    ],
  ]
]);

$res = $client->send($req);

$json = $res->json();

print "result status: " . $json['status'] . ", timestamp: " . $json['metadata']['date'] . "\n";

// imagine if we looked at all the results..
foreach ($json['results'] as $img) {
  print "id: " . $img['id'] . ", value: " . $img['result']['value'] . ", safe? - " . ($img['result']['safe'] ? 'true' : 'false') . "\n";
}
