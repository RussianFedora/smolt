Name: smolt
Summary: Fedora hardware profiler
Version: 0.5
Release: 2%{?dist}
License: GPL
Group: Applications/Internet
URL: http://hosted.fedoraproject.org/projects/smolt

# Note: This is a link to the gzip, you can't download it directly
# This will get fixed as soon as hosted can create attachments directly

Source: https://hosted.fedoraproject.org/projects/smolt/attachment/wiki/WikiStart/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch
Requires: /usr/bin/wget

%description
The Fedora hardware profiler is a server-client system that does a hardware
scan against a machine and sends the results to a public Fedora Project
turbogears server.  The sends are anonymous and should not contain any private
information other than the physical hardware information and basic OS info.

This package contains the client

%package server
Summary: Fedora hardware profiler server
Group: Applications/Internet
Requires: smolt = %{version}-%{release}
Requires: TurboGears

%description server
The Fedora hardware profiler is a server-client system that does a hardware
scan against a machine and sends the results to a public Fedora Project
turbogears server.  The sends are anonymous and should not contain any private
information other than the physical hardware information and basic OS info.

This package contains the server portion

%prep
%setup -q

%build

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m 0755 hardware/ %{buildroot}/%{_datadir}/%{name}/server/
%{__cp} -adv hardware/* %{buildroot}/%{_datadir}/%{name}/server/

%{__install} -d -m 0755 hw-client/ %{buildroot}/%{_datadir}/%{name}/client/
%{__cp} -adv hw-client/* %{buildroot}/%{_datadir}/%{name}/client/

%{__mkdir} -p %{buildroot}/%{_sysconfdir}/sysconfig/
touch %{buildroot}/%{_sysconfdir}/sysconfig/hw-uuid

%clean
rm -rf %{buildroot}

%post
if ! -f %{_sysconfdir}/sysconfig/hw-uuid
then
    /bin/cat /proc/sys/kernel/random/uuid > %{_sysconfdir}/sysconfig/hw-uuid
    /bin/chmod 0644 %{_sysconfdir}/sysconfig/hw-uuid
    /bin/chown root:root %{_sysconfdir}/sysconfig/hw-uuid
fi

%files
%defattr(-,root,root,-)
%doc README GPL 
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/client
%ghost %config(noreplace) %{_sysconfdir}/sysconfig/hw-uuid

%files server
%defattr(-,root,root,-)
%{_datadir}/%{name}/server

%changelog
* Thu Jan 22 2007 Mike McGrath <imlinux@gmail.com> 0.5-2
- s/turbogears/TurboGears/

* Thu Jan 22 2007 Mike McGrath <imlinux@gmail.com> 0.5-1
- Upstream released new version
- Fixed small bug in post

* Thu Jan 18 2006 Mike McGrath <imlinux@gmail.com> 0.4-2
- Added comment about the not directly available tar-gzip file

* Thu Jan 18 2006 Mike McGrath <imlinux@gmail.com> 0.4-1
- New upstream version
- Altered post install section
- Added wget requires

* Thu Jan 18 2006 Mike McGrath <imlinux@gmail.com> 0.3-1
- Upstream released new version

* Tue Jan 16 2006 Mike McGrath <imlinux@gmail.com> 0.2-1
- Initial Packaging
