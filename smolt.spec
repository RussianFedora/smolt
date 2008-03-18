Name: smolt
Summary: Fedora hardware profiler
Version: 1.1.1.1
Release: 2%{?dist}
License: GPL
Group: Applications/Internet
URL: http://hosted.fedoraproject.org/projects/smolt

# Note: This is a link to the gzip, you can't download it directly
# This will get fixed as soon as hosted can create attachments directly

Source: https://fedorahosted.org/releases/s/m/%{name}/%{name}-%{version}.tar.gz
Source1: smolt.py
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch
Requires: dbus-python, python-crypto, python-urlgrabber, gawk, python-genshi, python-paste
BuildRequires: gettext
BuildRequires: desktop-file-utils

Requires(pre): %{_sbindir}/groupadd
Requires(pre): %{_sbindir}/useradd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service

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
Requires: TurboGears mx

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

%package gui
Summary: Fedora hardware profiler gui
Group: Applications/Internet
Requires: smolt = %{version}-%{release}

%description gui
Provides smolt's gui functionality.  Not included in the default package to
ensure that deps are kept small.

%prep
%setup -q

%build
cd client/
make

%install
%{__rm} -rf %{buildroot}
cd client
DESTDIR=%{buildroot} make install
cd ..
%{__install} -d -m 0755 smoon/ %{buildroot}/%{_datadir}/%{name}/smoon/
%{__mkdir} -p %{buildroot}/%{_mandir}/man1/
%{__cp} -adv smoon/* %{buildroot}/%{_datadir}/%{name}/smoon/
%{__cp} -adv client/simplejson %{buildroot}/%{_datadir}/%{name}/client/
%{__cp} client/scan.py %{buildroot}/%{_datadir}/%{name}/client/
%{__cp} client/fs_util.py %{buildroot}/%{_datadir}/%{name}/client/
%{__cp} client/man/* %{buildroot}/%{_mandir}/man1/

%{__mkdir} -p %{buildroot}/%{_sysconfdir}/sysconfig/
%{__mkdir} -p %{buildroot}/%{_datadir}/firstboot/modules/
%{__mkdir} -p %{buildroot}/%{_initrddir}
#%{__mv} client/smoltFirstBoot.py %{buildroot}/%{_datadir}/firstboot/modules/smolt.py
%{__mv} %{SOURCE0} %{buildroot}/%{_datadir}/firstboot/modules/smolt.py
%{__mv} client/smolt-init %{buildroot}/%{_initrddir}/smolt

touch %{buildroot}/%{_sysconfdir}/sysconfig/hw-uuid

# Icons
%{__mkdir} -p %{buildroot}/%{_datadir}/icons/hicolor/16x16/apps/
%{__mkdir} -p %{buildroot}/%{_datadir}/icons/hicolor/22x22/apps/
%{__mkdir} -p %{buildroot}/%{_datadir}/icons/hicolor/24x24/apps/
%{__mkdir} -p %{buildroot}/%{_datadir}/icons/hicolor/32x32/apps/
%{__mkdir} -p %{buildroot}/%{_datadir}/firstboot/pixmaps/
%{__mkdir} -p %{buildroot}/%{_datadir}/firstboot/themes/default/
%{__mv} client/icons/smolt-icon-16.png %{buildroot}/%{_datadir}/icons/hicolor/16x16/apps/smolt.png
%{__mv} client/icons/smolt-icon-22.png %{buildroot}/%{_datadir}/icons/hicolor/22x22/apps/smolt.png
%{__mv} client/icons/smolt-icon-24.png %{buildroot}/%{_datadir}/icons/hicolor/24x24/apps/smolt.png
%{__mv} client/icons/smolt-icon-32.png %{buildroot}/%{_datadir}/icons/hicolor/32x32/apps/smolt.png
%{__cp} -adv client/icons/* %{buildroot}/%{_datadir}/%{name}/client/icons/
%{__cp} -adv client/icons/smolt-icon-48.png %{buildroot}/%{_datadir}/firstboot/themes/default/smolt.png

%{__rm} -f %{buildroot}/%{_bindir}/smoltSendProfile %{buildroot}/%{_bindir}/smoltDeleteProfile %{buildroot}/%{_bindir}/smoltGui
ln -s %{_datadir}/%{name}/client/sendProfile.py %{buildroot}/%{_bindir}/smoltSendProfile
ln -s %{_datadir}/%{name}/client/deleteProfile.py %{buildroot}/%{_bindir}/smoltDeleteProfile
ln -s %{_datadir}/%{name}/client/smoltGui.py %{buildroot}/%{_bindir}/smoltGui
ln -s %{_sysconfdir}/%{name}/config.py %{buildroot}/%{_datadir}/%{name}/client/config.py

desktop-file-install --vendor='fedora' --dir=%{buildroot}/%{_datadir}/applications client/smolt.desktop
%find_lang %{name}

# Cleanup from the Makefile (will be cleaned up when it is finalized)
%{__rm} -f %{buildroot}/etc/init.d/smolt
%{__rm} -f %{buildroot}/etc/smolt/hw-uuid

%clean
rm -rf %{buildroot}

%pre
%{_sbindir}/groupadd -r %{name} &>/dev/null || :
%{_sbindir}/useradd  -r -s /sbin/nologin -d %{_datadir}/%{name} -M \
                               -c 'Smolt' -g %{name} %{name} &>/dev/null || :

%post
/sbin/chkconfig --add smolt

#Randomize checkin times.
TMPFILE=$(/bin/mktemp /tmp/smolt.XXXXX)
/bin/awk '{ srand(); if($2 == 1 && $3 == 1) print $1,int((rand() * 100) % 22 + 1),int((rand() * 100) % 27 + 1),substr($0,index($0,$4)); else print $0}' /etc/cron.d/smolt > $TMPFILE
/bin/cp $TMPFILE /etc/cron.d/smolt
/bin/rm -f $TMPFILE

%preun
if [ $1 = 0 ]; then
        /sbin/service smolt stop >/dev/null 2>&1
        /sbin/chkconfig --del smolt
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README GPL doc/*
%dir %{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}/
%{_datadir}/%{name}/client
%{_datadir}/%{name}/doc
%{_bindir}/smoltSendProfile
%{_bindir}/smoltDeleteProfile
%config(noreplace) /%{_sysconfdir}/%{name}/config*
%{_sysconfdir}/cron.d/%{name}
%{_mandir}/man1/*gz
%{_initrddir}/%{name}
%ghost %config(noreplace) %{_sysconfdir}/sysconfig/hw-uuid

%files server
%defattr(-,root,root,-)
%{_datadir}/%{name}/smoon

%files firstboot
%defattr(-,root,root,-)
%{_datadir}/firstboot/modules/smolt.py*
%{_datadir}/firstboot/themes/default/smolt.png

%files gui
%defattr(-,root,root,-)
%{_datadir}/applications/fedora-smolt.desktop
%{_datadir}/icons/hicolor/*x*/apps/smolt.png
%{_bindir}/smoltGui

%changelog
* Sat Mar 08 2008 Mike McGrath <mmcgrath@redhat.com> - 1.1.1.1-2
- Fix firstboot for 437708, 437765

* Sat Mar 08 2008 Mike McGrath <mmcgrath@redhat.com> - 1.1.1.1-1
- Upstream released new version

* Wed Mar 05 2008 Mike McGrath <mmcgrath@redhat.com> - 1.1.1-1
- Upstream released new version
- Manfiles added
- Source location updated

* Wed Feb 27 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.1-3
- Copy instead of move cron file so that selinux contexts are set
  properly. (BZ#435050)

* Wed Feb 27 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.1-2
- Create smolt user. (BZ#435136)

* Fri Feb 01 2008 Mike McGrath <mmcgrath@redhat.com> 1.0-5
- Added a req for mx on smoon

* Thu Jan 08 2008 Mike McGrath <mmcgrath@redhat.com> 1.0-4
- Fixed firstboot

* Thu Jan 08 2008 Mike McGrath <mmcgrath@redhat.com> 1.0-3
- Added python-urlgrabber as a requires - 427969

* Thu Nov 22 2007 Mike McGrath <mmcgrath@redhat.com> 1.0-2
- Installed scanner - #395901

* Tue Nov 20 2007 Mike McGrath <mmcgrath@redhat.com> 1.0-1
- Upstream released new version

* Tue Oct 25 2007 Mike McGrath <mmcgrath@redhat.com> 0.9.9.2-1
- Upstream released new version

* Tue Oct 23 2007 Mike McGrath <mmcgrath@redhat.com> 0.9.9.1-4
- Upstream released new version

* Thu Oct 18 2007 Mike McGrath <mmcgrath@redhat.com> 0.9.9-2
- Fixed /etc/smolt/ ownership issue

* Tue Oct 16 2007 Mike McGrath <mmcgrath@redhat.com> 0.9.9-1
- Upstream released new version

* Fri Sep 28 2007 Mike McGrath <mmcgrath@redhat.com> 0.9.8.4-8
- Fixed Selinux

* Thu Sep 27 2007 Mike McGrath <mmcgrath@redhat.com> 0.9.8.4-6
- Added translations

* Fri Sep 21 2007 Mike McGrath <mmcgrath@redhat.com> 0.9.8.4-5
- Fixed firstboot issues

* Mon Aug 13 2007 Mike McGrath <mmcgrath@redhat.com> 0.9.8.4-4
- Rebuild to clean up 'config.py' compilations

* Mon Aug 13 2007 Mike McGrath <mmcgrath@redhat.com> 0.9.8.4-1
- Upstream released new version (major changes)
- New config file
- New Makefile
- Added deps

* Fri Jun 22 2007 Mike McGrath <mmcgrath@redhat.com> 0.9.8.3
- Upstream released new version

* Thu May 24 2007 Mike McGrath <mmcgrath@redhat.com> - 0.9.8.1
- Upstream released new version

* Sun Apr 22 2007 Mike McGrath <mmcgrath@redhat.com> - 0.9.7.1-3
- Added smolt icons

* Tue Apr 17 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.6-4
- Add standard scriptlets in pre & post to handle init script - fixes #236776
- Use the find_lang macro to find/mark translations.

* Fri Apr 13 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.6-3
- Put a copy of the privacy policy where the client is expecting it.

* Wed Apr 11 2007 Mike McGrath <mmcgrath@redhat.com> 0.9.6-2
- Upstream released new version.
- Much better support for languages on the client

* Fri Mar 16 2007 Mike McGrath <mmcgrath@redhat.com> 0.9.4-1
- Upstream released new version
- Major changes
- Added initial i18n support (Probably doesn't work)

* Fri Mar 01 2007 Mike McGrath <mmcgrath@redhat.com> 0.9.2-1
- Fixed firstboot
- Upstream released new version

* Fri Mar 01 2007 Mike McGrath <mmcgrath@redhat.com> 0.9.1-1
- Upstream released new version, major smoon changes.

* Mon Feb 19 2007 Mike McGrath <mmcgrath@redhat.com> 0.9-1
- Upstream released new version

* Mon Feb 12 2007 Mike McGrath <imlinux@gmail.com> 0.8-1
- New version released, major changes in both server and client

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
