%define upstream_name    DJabberd
%define upstream_version 0.84

# TODO generate

Name:		perl-%{upstream_name}
Version:	%perl_convert_version %{upstream_version}
Release:	4

Summary:	XMPP flexible framework to create custom jabber server
License:	GPL+ and Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{upstream_name}
Source0:	http://www.cpan.org/modules/by-module/DJabberd/%{upstream_name}-%{upstream_version}.tar.gz
Source1:	djabberd.init
Source2:	djabberd.conf
Source3:	djabberd.sysconfig
Source4:	djabberd.log.conf
Source5:	djabberd.logrotate

BuildRequires:	perl-devel
BuildRequires:	perl(Danga::Socket)
BuildRequires:	perl(Log::Log4perl)
BuildRequires:	perl(XML::LibXML)
BuildRequires:	perl(Digest::SHA1)
BuildRequires:	perl(XML::SAX)
BuildRequires:	perl(Net::DNS)
BuildRequires:	perl(Net::SSLeay)
BuildArch:	noarch

%description
DJabberd is a high-performance, scalable, extensible Jabber/XMPP server
framework.
While it comes with an example server, it's really a set of classes for
you to build your own Jabber server without understanding Jabber.
Instead of working with XML and protocol-specific details, you subclass parts
and work
with sane objects and data structures and let DJabberd do all the ugly work.

%package -n djabberd
Summary:	A jabber server, constructed with DJabber perl framework
Group:		System/Servers
Requires(preun): rpm-helper
Requires(post): rpm-helper

%description -n djabberd
This package contains a example djabberd server, using the simplest possible
modules ( ie, everything is stored in memory, no persistance )
It is not intended to be used as it is, it just provides the needed example
file and infrastructure to be integrated with the distribution.

In order to turn this into a real server, you need to install various modules,
depending on your needs.

%prep
%setup -q -n %{upstream_name}-%{upstream_version}
mkdir -p doc/DJabberd/Component/
# do notprovides it, as it pulls a non packaged module
#mv ./lib/DJabberd/Component/Example.pm doc/DJabberd/Component/
rm -f ./lib/DJabberd/Component/Example.pm

%build
perl Makefile.PL INSTALLDIRS=vendor
%make

%check
export T_MUC_ENABLE=0
make test

%install
%makeinstall_std

mkdir -p %{buildroot}%{_initrddir}/
cp %{SOURCE1} %{buildroot}%{_initrddir}/djabberd

mkdir -p %{buildroot}%{_sysconfdir}/djabberd/
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/djabberd

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/djabberd

# logging
cp %{SOURCE4} %{buildroot}%{_sysconfdir}/djabberd/log.conf

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
cp %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/djabberd

%post -n djabberd
%_post_service djabberd

%preun -n djabberd
%_preun_service djabberd

%files -n djabberd
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_initrddir}/djabberd
%config(noreplace) %{_sysconfdir}/djabberd
%config(noreplace) %{_sysconfdir}/sysconfig/djabberd
%config(noreplace) %{_sysconfdir}/logrotate.d/*

%files
%doc doc/*
%{perl_vendorlib}/DJabberd*
%{_mandir}/man3/*

%changelog
* Wed Jul 08 2009 Jérôme Quelin <jquelin@mandriva.org> 0.840.0-1mdv2010.0
+ Revision: 393669
- update to 0.84
- using %%perl_convert_version
- removing patch djabberd.fix_5.10.diff merged upstream
- fixed license field

* Fri Sep 26 2008 Michael Scherer <misc@mandriva.org> 0.83-4mdv2009.0
+ Revision: 288537
- whitespace cleaning
- add patch for perl 5.10 from upstream svn

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed May 09 2007 Michael Scherer <misc@mandriva.org> 0.83-1mdv2008.0
+ Revision: 25425
- version 0.83
- remove patch1, applied upstream


* Tue Nov 14 2006 Michael Scherer <misc@mandriva.org> 0.81-1mdv2007.0
+ Revision: 83963
- add missing BuildRequires Net/SSLeay
- fix typo in previous commit
- add missing BuildRequires Net:DNS
- missing BuildRequires Digest::SHA1
- add missing buildrequires XML/LibXML.pm
- enhance initscript to be able to define PERL5LIB in sysconfig file
- missing buildrequires
- add more comment about default config values
- add patch for pidfile, from subversion
- remove patch about test and muc, integrated upstream with 0.81
- do not forget to kill the daemon in stop action
- pidfile should be outside of the Vhost directive
- add configuration for PidFile ( as pointed by Martin Atkins )
- fix various rpmlint error, add a description, and service reload.
- add a log file, and a logrotate file
- really use a initscript configfile
- use a configuration file for initscript ( and also fix it, ie, use djabberd, not ejabberd )
- do not provides the file DJabberd/Component/Example.pm, as it pulls Bot::Eliza, even if placed
  in %%doc
- rewrite the config file to be working out of the box ( without any real functionnality however, as it requires
  plugin not yet released except in djabber svn )
- use the correct option
- Import perl-DJabberd

