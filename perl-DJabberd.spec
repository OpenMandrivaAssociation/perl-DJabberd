# TODO generate 

%define module  DJabberd
%define name    perl-%{module}
%define version 0.81
%define release %mkrel 1

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        XMPP flexible framework to create custom jabber server 
License:        GPL and Artistic
Group:          Development/Perl
URL:            http://search.cpan.org/dist/%{module}
Source:         http://www.cpan.org/modules/by-module/DJabberd/%{module}-%{version}.tar.bz2
Source1:        djabberd.init
Source2:        djabberd.conf
Source3:        djabberd.sysconfig
Source4:        djabberd.log.conf
Source5:        djabberd.logrotate
# taken from svn
Patch1:          djabberd-pid_file.patch
%if %{mdkversion} < 1010
BuildRequires:  perl-devel
%endif
BuildRequires: perl(Danga::Socket) 
BuildRequires: perl(Log::Log4perl) 
BuildRequires: perl(XML::LibXML) 
BuildRequires: perl(Digest::SHA1) 
BuildRequires: perl(XML::SAX)
BuildRequires: perl(Net::DNS)
BuildRequires: perl(Net::SSLeay) 
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
DJabberd is a high-performance, scalable, extensible Jabber/XMPP server 
framework. 
While it comes with an example server, it's really a set of classes for 
you to build your own Jabber server without understanding Jabber. 
Instead of working with XML and protocol-specific details, you subclass parts 
and work 
with sane objects and data structures and let DJabberd do all the ugly work.

%package -n djabberd
Summary:  A jabber server, constructed with DJabber perl framework 
Group:    System/Servers
Requires(preun): rpm-helper
Requires(post):  rpm-helper
%description -n djabberd
This package contains a example djabberd server, using the simplest possible 
modules ( ie, everything is stored in memory, no persistance )
It is not intended to be used as it is, it just provides the needed example 
file and infrastructure to be integrated with the distribution.

In order to turn this into a real server, you need to install various modules, 
depending on your needs.

%prep
%setup -q -n %{module}-%{version} 
%patch1 -p0
mkdir -p doc/DJabberd/Component/
# do notprovides it, as it pulls a non packaged module
#mv ./lib/DJabberd/Component/Example.pm doc/DJabberd/Component/
rm -f ./lib/DJabberd/Component/Example.pm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make

%check
export T_MUC_ENABLE=0
%{__make} test

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p $RPM_BUILD_ROOT/%{_initrddir}/
cp %SOURCE1 $RPM_BUILD_ROOT/%{_initrddir}/djabberd

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/djabberd/
cp %SOURCE2 $RPM_BUILD_ROOT/%{_sysconfdir}/djabberd

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/
cp %SOURCE3 $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/djabberd

# logging
cp %SOURCE4 $RPM_BUILD_ROOT/%{_sysconfdir}/djabberd/log.conf

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/
cp %SOURCE5 $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/djabberd

mkdir -p $RPM_BUILD_ROOT/
%clean
rm -rf %{buildroot}

%post -n djabberd
%_post_service djabberd

%preun -n djabberd
%_preun_service djabberd

%files -n djabberd
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_initrddir}/djabberd
%config(noreplace) %{_sysconfdir}/djabberd
%config(noreplace) %{_sysconfdir}/sysconfig/djabberd
%config(noreplace) %{_sysconfdir}/logrotate.d/*

%files
%defattr(-,root,root)
%doc doc/*
%{perl_vendorlib}/DJabberd*
%{_mandir}/man3/*


