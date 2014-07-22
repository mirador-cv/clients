use strict;
use warnings;

package Mirador;
use Mojo::UserAgent;
use Mojo::URL;
use MIME::Base64;

use constant {
  BASE_URI => 'http://api.mirador.im/v1/classify'
};

sub new {
  my ($class, $key) = @_;

  my $self = {
    _apikey => $key,
    _ua => Mojo::UserAgent->new,
  };

  bless $self, $class;

  $self;
}

sub _ua {
  scalar(shift())->{_ua};
}

sub _url {
  Mojo::URL->new(BASE_URI);
}

sub _default {
  my ($self, %opt) = @_;
  $opt{api_key} = $self->{_apikey};

  return \%opt;
}

sub _process {
  my ($self, $f) = @_;

  open FN, '<', $f or die "could not open file $f: $!";
  my $raw = do{ local $/=undef; <FN>; };
  close FN;

  return if !$raw;
  # encode it to base64
  my $encoded = encode_base64($raw);
  $encoded =~ s/[\n\r]//g;

  return $encoded;
}

sub _parse_results {
  my ($self, $names, $results) = @_;

  my @r = map {
    my $r = $results->[$_]->{result};
    {name=> $names->[$_], value => $r->{value}, safe => $r->{safe}}
  } 0..(scalar(@$results) - 1);

  return \@r;
}

sub classify_urls {
  my ($self, @urls) = @_;

  my $url = $self->_url;
  $url->query($self->_default(url => @urls));

  my $res = $self->_ua->get($url)->res->json;
  return $res if $res->{errors};

  return $self->_parse_results(\@urls, $res->{results});
}

sub classify_files {
  my ($self, @files) = @_;

  my @images = map { $self->_process($_); } @files;

  return $self->classify_base64(\@files, \@images);
}

sub classify_base64 {
  my ($self, $files, $strs) = @_;
  my $url = $self->_url;

  open EX_FILE, '>', 'b64_test_out.txt';
  print EX_FILE "$strs->[0]\n";
  close EX_FILE;


  my $res = $self->_ua->post(
    $url, form => $self->_default(image => $strs),
  )->res->json;

  return $res if $res->{errors};

  return $self->_parse_results($files, $res->{results});
}

unless (caller) {
  use Data::Dumper;

  my $mirador = Mirador->new('your_api_key');
  print $mirador;

  my $res = $mirador->classify_files(@ARGV);
  print Dumper($res);

}

1;
