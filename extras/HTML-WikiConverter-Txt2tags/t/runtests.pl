#!/usr/bin/perl
use warnings;
use strict;

use Test::More;
use File::Spec;
use HTML::Entities;
use HTML::WikiConverter;
*e = \&encode_entities;

my $more_tests = <<END_TESTS;
__NEXT__
entities (1)
__H__
To enter a '&lt;' in your input, use "&amp;lt;"
__W__
To enter a '&lt;' in your input, use "&amp;lt;"
__NEXT__
entities (2)
__H__
To enter a '<' in your input, use "&amp;lt;"
__W__
To enter a '&lt;' in your input, use "&amp;lt;"
__NEXT__
strip comments
__H__
A <!-- stripped --> comment
__W__
A  comment
__NEXT__
strip head
__H__
<html>
<head><title>fun stuff</title></head>
<body>
<p>Crazy stuff here</p>
</body>
</html>
__W__
Crazy stuff here
__NEXT__
strip scripts
__H__
<html>
<head><script>bogus stuff</script></head>
<body>
<script>maliciousCode()</script>
<p>benevolent text</p>
</body>
</html>
__W__
benevolent text
END_TESTS

sub runtests {
  my %arg = @_;

  $arg{wrap_in_html} = 1;
  $arg{base_uri} ||= 'http://www.test.com';
  my $minimal = $arg{minimal} || 0;

  my $data = $arg{data} || '';
  $data .= entity_tests() . $more_tests unless $minimal;

  my @tests = split /__NEXT__\n/, $data;
  my $numtests = @tests;
  #$numtests += 1 unless $minimal; # file test
  plan tests => $numtests;

  # Delete unrecognized HTML::WikiConverter options
  delete $arg{$_} for qw/ data minimal /;

  my $wc = new HTML::WikiConverter(%arg);
  foreach my $test ( @tests ) {
    $test =~ s/^(.*?)\n//; my $name = $1;
    my( $html, $wiki ) = split /__W__\n/, $test;
    $html =~ s/__H__\n//;

    $name =~ s{\s*\:\:(\w+\([^\)]*?\))}{
      my $method_call = $1;
      eval "\$wc->$method_call;";
      die "Failed test call ($name): $@" if $@;
      '';
    }ge;

    for( $html, $wiki ) { s/^\n+//; s/\n+$// }
    is( $wc->html2wiki($html), $wiki, $name );
  }

  #file_test($wc) unless $minimal;
}

sub entity_tests {
  my $tmpl = "__NEXT__\n%s\n__H__\n%s\n__W__\n%s\n"; # test-name, html-input, expected-wiki-output

  my $data = '';
  my @chars = ( '<', '>', '&' );
  foreach my $char ( @chars ) {
    ( my $charname = e($char) ) =~ s/[&;]//g;
    $data .= sprintf $tmpl, "literal ($charname)", $char, e($char)
          .  sprintf $tmpl, "encode ($charname)", e($char), e($char)
          .  sprintf $tmpl, "meta ($charname)", e(e($char)), e(e($char));
  }

  return $data;
}

sub _slurp {
  my $path = shift;
  open H, $path or die "couldn't open $path: $!";
  local $/;
  my $c = <H>;
  close H;
  return $c;
}

sub file_test {
  my $wc = shift;
  my $lc_dialect = lc $wc->dialect;
  my $infile = File::Spec->catfile( 't', 'complete.html' );
  my $outfile = File::Spec->catfile( 't', "complete.$lc_dialect" );

  SKIP: {
    skip "Couldn't find $infile (ignore this)", 1 unless -e $infile;
    skip "Couldn't find $outfile (ignore this)", 1 unless -e $outfile;
    my( $got, $expect ) = ( $wc->html2wiki( file => $infile, slurp => 1 ), _slurp($outfile) );
    for( $got, $expect ) { s/^\n+//; s/\n+$// }
    is( $got, $expect, 'read from file' );
  };
}

1;
