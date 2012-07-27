package HTML::WikiConverter::DokuWiki;

use warnings;
use strict;

use base 'HTML::WikiConverter';

our $VERSION = '0.53';

=head1 NAME

HTML::WikiConverter::DokuWiki - Convert HTML to DokuWiki markup

=head1 SYNOPSIS

  use HTML::WikiConverter;
  my $wc = new HTML::WikiConverter( dialect => 'DokuWiki' );
  print $wc->html2wiki( $html );

=head1 DESCRIPTION

This module contains rules for converting HTML into DokuWiki
markup. See L<HTML::WikiConverter> for additional usage details.

=head1 ATTRIBUTES

In addition to the regular set of attributes recognized by the
L<HTML::WikiConverter> constructor, this dialect also accepts the
following attributes:

=head2 camel_case

Boolean indicating whether CamelCase links are enabled in the target DokuWiki
instance. Enabling CamelCase links will turn HTML like this

  <p><a href="/wiki:camelcase">CamelCase</a> links are fun.</p>

into this DokuWiki markup:

  CamelCase links are fun.

Disabling CamelCase links (the default) would convert that HTML into

  [[CamelCase]] links are fun.

=cut

sub attributes { {
  camel_case => { default => 0 }
} }

sub rules {
  my %rules = (
    b => { start => '**', end => '**' },
    strong => { alias => 'b' },
    i => { start => '//', end => '//' },
    em => { alias => 'i' },
    u => { start => '__', end => '__' },

    tt => { start => '"', end => '"' },
    code => { alias => 'tt' },
    a => { replace => \&_link },
    img => { replace => \&_image },

    pre => { line_format => 'blocks', line_prefix => '  ', block => 1 },
    blockquote => { start => "\n", line_prefix => '>', block => 1, line_format => 'multi', trim => 'leading' },

    p => { block => 1, trim => 'both', line_format => 'multi' },
    br => { replace => "\\\\ " },
    hr => { replace => "\n----\n" },

    sup => { preserve => 1 },
    sub => { preserve => 1 },
    del => { preserve => 1 },

    ul => { line_format => 'multi', block => 1, line_prefix => '  ' },
    ol => { alias => 'ul' },
    li => { line_format => 'multi', start => \&_li_start, trim => 'leading' },

    table => { block => 1 },
    tr => { start => "\n", line_format => 'single' },
    td => { start => \&_td_start, end => \&_td_end, trim => 'both' },
    th => { alias => 'td' },
  );

  for( 1..5 ) {
    my $str = ( '=' ) x (7 - $_ );
    $rules{"h$_"} = { start => "$str ", end => " $str", block => 1, trim => 'both', line_format => 'single' };
  }
  $rules{h6} = { start => '== ', end => ' ==', block => 1, trim => 'both', line_format => 'single' };

  return \%rules;
}

sub postprocess_output {
  my( $self, $outref ) = @_;
  $$outref =~ s~^>+\s+~~gm; # rm empty blockquote prefixes
  $$outref =~ s~^(>+)~$1 ~gm; # add space after prefix for clarity
}

sub _li_start {
  my( $self, $node, $rules ) = @_;
  my @parent_lists = $node->look_up( _tag => qr/ul|ol/ );

  my $bullet = '';
  $bullet = '*' if $node->parent->tag eq 'ul';
  $bullet = '-' if $node->parent->tag eq 'ol';

  return "\n$bullet ";
}

sub _link {
  my( $self, $node, $rules ) = @_;
  my $url = $node->attr('href') || '';
  my $text = $self->get_elem_contents($node) || '';
  
  if( my $title = $self->get_wiki_page($url) ) {
    # [[MiXed cAsE]] ==> <a href="http://site/wiki:mixed_case">MiXed cAsE</a>
    $title =~ s/_/ /g;
    return $text if $self->camel_case and lc $title eq lc $text and $self->is_camel_case($text);
    return "[[$text]]" if lc $text eq lc $title;
    return "[[$title|$text]]";
  } else {
    return $url if $url eq $text;
    return "[[$url|$text]]";
  }
}

sub _image {
  my( $self, $node, $rules ) = @_;
  my $src = $node->attr('src') || '';
  return '' unless $src;

  my $w = $node->attr('width') || 0;
  my $h = $node->attr('height') || 0;
  if( $w and $h ) {
    $src .= "?${w}x${h}";
  } elsif( $w ) {
    $src .= "?${w}";
  }

  my $class = $node->attr('class') || '';
  my $padleft = $class eq 'mediaright' || $class eq 'mediacenter' ? ' ' : '';
  my $padright = $class eq 'medialeft' || $class eq 'mediacenter' ? ' ' : '';
  $src = "$padleft$src$padright";

  # All images considered external
  my $caption = $node->attr('title') || $node->attr('alt') || '';
  return "{{$src|$caption}}" if $caption;
  return "{{$src}}";
}

sub _td_start {
  my( $self, $node, $rules ) = @_;
  my $prefix = $node->tag eq 'th' ? '^' : '|';
  $prefix .= ' ';

  my $class = $node->attr('class') || '';
  $prefix .= ' ' if $class eq 'rightalign' or $class eq 'centeralign';

  return $prefix;
}

sub _td_end {
  my( $self, $node, $rules ) = @_;

  my $end = ' ';

  my $class = $node->attr('class') || '';
  $end .= ' ' if $class eq 'leftalign' or $class eq 'centeralign';

  my $colspan = $node->attr('colspan') || 1;

  my @right_cells = grep { $_->tag && $_->tag =~ /th|td/ } $node->right;
  return $end if $colspan == 1 and @right_cells;

  my $suffix = $node->tag eq 'th' ? '^' : '|';
  $suffix = ( $suffix ) x $colspan;
  return $end.$suffix;
}

=head1 AUTHOR

David J. Iberri, C<< <diberri at cpan.org> >>

=head1 BUGS

Please report any bugs or feature requests to
C<bug-html-wikiconverter-dokuwiki at rt.cpan.org>, or through the web
interface at
L<http://rt.cpan.org/NoAuth/ReportBug.html?Queue=HTML-WikiConverter-DokuWiki>.
I will be notified, and then you'll automatically be notified of
progress on your bug as I make changes.

=head1 SUPPORT

You can find documentation for this module with the perldoc command.

    perldoc HTML::WikiConverter::DokuWiki

You can also look for information at:

=over 4

=item * AnnoCPAN: Annotated CPAN documentation

L<http://annocpan.org/dist/HTML-WikiConverter-DokuWiki>

=item * CPAN Ratings

L<http://cpanratings.perl.org/d/HTML-WikiConverter-DokuWiki>

=item * RT: CPAN's request tracker

L<http://rt.cpan.org/NoAuth/Bugs.html?Dist=HTML-WikiConverter-DokuWiki>

=item * Search CPAN

L<http://search.cpan.org/dist/HTML-WikiConverter-DokuWiki>

=back

=head1 COPYRIGHT & LICENSE

Copyright 2006 David J. Iberri, all rights reserved.

This program is free software; you can redistribute it and/or modify
it under the same terms as Perl itself.

=cut

1;
