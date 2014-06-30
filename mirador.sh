#!/usr/bin/env bash
# Mirador Image Moderation API examples
# mirador.im
###

# classify a url; just do a simple GET request
curl "http://api.mirador.im/v1/classify?api_key=YOUR_KEY_HERE&url=http://nude-pix.com/1.jpg&url=http://possibly-unsafe.co/party-pix.png"
  | python -m json.tool

# to upload image(s), convert it to base64
curl -X POST -d "api_key=YOUR_KEY_HERE&image=$(cat test_image.png | base64)" "http://api.mirador.im/v1/classify"
  | python -m json.tool
