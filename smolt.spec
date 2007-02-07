Name: smolt
Summary: Fedora hardware profiler
Version: 0.7
Release: 1%{?dist}
License: GPL
Group: Applications/Internet
URL: http://hosted.fedoraproject.org/projects/smolt

# Note: This is a link to the gzip, you can't download it directly
# This will get fixed as soon as hosted can create attachments directly

Source: https://hosted.fedoraproject.org/projects/smolt/attachment/wiki/WikiStart/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch
Requires: dbus-python

# If firstboot is installed
#Requires: firstboot

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

%package firstboot
Summary: Fedora hardware profile firstboot
Group: Applications/Internet
Requires: smolt = %{version}-%{release}

%description firstboot
This provides firstboot integration for smolt.  It has been broken into a
separate package so firstboot isn't a requisite to use smolt.

%prep
%setup -q

%build

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m 0755 smoon/ %{buildroot}/%{_datadir}/%{name}/smoon/
%{__cp} -adv smoon/* %{buildroot}/%{_datadir}/%{name}/smoon/

%{__install} -d -m 0755 client/ %{buildroot}/%{_datadir}/%{name}/client/
%{__cp} -adv client/* %{buildroot}/%{_datadir}/%{name}/client/

%{__mkdir} -p %{buildroot}/%{_sysconfdir}/sysconfig/
%{__mkdir} -p %{buildroot}/%{_bindir}
%{__mkdir} -p %{buildroot}/%{_datadir}/firstboot/modules/
%{__cp} -adv firstboot/smolt.py %{buildroot}/%{_datadir}/firstboot/modules/
touch %{buildroot}/%{_sysconfdir}/sysconfig/hw-uuid

ln -s %{_datadir}/%{name}/client/sendProfile.py %{buildroot}/%{_bindir}/smoltSendProfile
%{__chmod} +x %{buildroot}/%{_datadir}/%{name}/client/sendProfile.py

%clean
rm -rf %{buildroot}

%post
if ! [ -f %{_sysconfdir}/sysconfig/hw-uuid ]
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
%{_bindir}/%{name}*
%ghost %config(noreplace) %{_sysconfdir}/sysconfig/hw-uuid

%files server
%defattr(-,root,root,-)
%{_datadir}/%{name}/smoon

%files firstboot
%defattr(-,root,root,-)
%{_datadir}/firstboot/modules/smolt.py*

%changelog
* Wed Feb 07 2007 Mike McGrath <imlinux@gmail.com> 0.7-1
- Upstream released new version

* Tue Jan 31 2007 Mike McGrath <imlinux@gmail.com> 0.6.2-1
- Upstream released new version (bug in firstboot)

* Tue Jan 30 2007 Mike McGrath <imlinux@gmail.com> 0.6.1-3
- Removed LSB requirement for sparc

* Tue Jan 30 2007 Mike McGrath <imlinux@gmail.com> 0.6.1-2
- Added firstboot
- Upstream released new version

* Mon Jan 29 2007 Mike McGrath <imlinux@gmail.com> 0.6-1
- Upstream released new version
- Added new symlinks for smoltPrint and smoltSendProfile

* Thu Jan 25 2007 Mike McGrath <imlinux@gmail.com> 0.5-4
- Forgot Requires of dbus-python

* Wed Jan 24 2007 Mike McGrath <imlinux@gmail.com> 0.5-3
- Fixed silly bash syntax error

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
