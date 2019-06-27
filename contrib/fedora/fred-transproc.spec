%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%define debug_package %{nil}

Summary: FRED TransProc
Name: fred-transproc
Version: %{our_version}
Release: %{?our_release}%{!?our_release:1}%{?dist}
Source0: %{name}-%{version}.tar.gz
License: GPLv3+
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: CZ.NIC <fred@nic.cz>
Url: https://fred.nic.cz/
BuildRequires: python-setuptools
Requires: python python-dateutil python2-zeep

%description
Component of FRED (Fast Registry for Enum and Domains)

%prep
%setup -n %{name}-%{version}

%install
python2 setup.py install -cO2 --force --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES --prefix=/usr

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/fred/
install examples/transproc.conf $RPM_BUILD_ROOT/%{_sysconfdir}/fred/

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/fred-transproc/
install ChangeLog $RPM_BUILD_ROOT/%{_docdir}/fred-transproc/
install README $RPM_BUILD_ROOT/%{_docdir}/fred-transproc/
install doc/backend.xml $RPM_BUILD_ROOT/%{_docdir}/fred-transproc/

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%config %{_sysconfdir}/fred/transproc.conf
%docdir %{_docdir}/fred-transproc/
%{_docdir}/fred-transproc/
