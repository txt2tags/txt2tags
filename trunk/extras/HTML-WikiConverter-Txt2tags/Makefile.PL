use strict;
use warnings;
use ExtUtils::MakeMaker;

WriteMakefile(
    NAME                => 'HTML::WikiConverter::Txt2tags',
    AUTHOR              => 'Eric Forgeot',
    VERSION_FROM        => 'lib/HTML/WikiConverter/Txt2tags.pm',
    ABSTRACT_FROM       => 'lib/HTML/WikiConverter/Txt2tags.pm',
    PL_FILES            => {},
    PREREQ_PM => {
#        'Test::More' => 0,
        'HTML::WikiConverter' => 0.68,
    },
    dist                => { COMPRESS => 'gzip -9f', SUFFIX => 'gz', },
    clean               => { FILES => 'HTML-WikiConverter-Txt2tags-*' },
);
