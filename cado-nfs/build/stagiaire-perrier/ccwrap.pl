#!/usr/bin/env perl

use warnings;
use strict;

my $want_cxx = ($0 =~ 'cxxwrap');

my @default_cc = qw{/usr/bin/cc};
my @mpi_cc = qw{/usr/bin/cc};
my @default_cxx = qw{/usr/bin/c++};
my @mpi_cxx = qw{/usr/bin/c++};

my $compiler_name = $want_cxx ? 'c++' : 'cc';
my @default_compiler = $want_cxx ? @default_cxx : @default_cc;
my @mpi_compiler = $want_cxx ? @mpi_cxx : @mpi_cc;

sub usage {
    print STDERR <<EOF;
Usage: $0 [command line arguments...]

This really wraps around the original $compiler_name, as the expansion is:

@default_compiler [command line arguments...]

However, if an argument --mpi is found, then the command line becomes

@mpi_compiler [command line arguments...] (with the --mpi removed)
EOF
    exit 1;
}

# scan to see if we have -c or -S somewhere

# if we have no -c, then we're linking, in which case we _want_ a c++ linker
# because there might be c++ object files in some of the linked libs.

my $compiling = scalar grep(/^-[cS]$/, @ARGV);

if (!$compiling) {
	$want_cxx = 1;
	@default_compiler = $want_cxx ? @default_cxx : @default_cc;
	@mpi_compiler = $want_cxx ? @mpi_cxx : @mpi_cc;
}

my @compiler = @default_compiler;

my @args = ();
my @prepend;

my $compile = 0;
while (defined($_=shift @ARGV)) {
    /^--mpi$/ && do {
        @compiler = @mpi_compiler;
	@prepend = ($want_cxx ?
			 split(';', '')
			:
			 split(';', ''));
        # print STDERR "Using @compiler instead of @default_compiler\n";
        next;
    };
    push @args, $_;
}

usage unless scalar @args;

unshift @args, @prepend;

# print "$compiler ", join(" ", @args), "\n";

exec @compiler, @args;
