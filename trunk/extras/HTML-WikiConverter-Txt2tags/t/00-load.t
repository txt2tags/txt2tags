#!perl -T

use Test::More tests => 1;

BEGIN {
	use_ok( 'HTML::WikiConverter::Txt2tags' );
}

diag( "Testing HTML::WikiConverter::Txt2tags $HTML::WikiConverter::Txt2tags::VERSION, Perl $], $^X" );
