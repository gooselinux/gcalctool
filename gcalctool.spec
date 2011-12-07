Name:           gcalctool
Version:        5.28.2
Release:        3%{?dist}
Summary:        A desktop calculator

Group:          Applications/System
License:        GPLv2+
URL:            http://directory.fsf.org/gcalctool.html
Source0:        http://download.gnome.org/sources/gcalctool/5.28/gcalctool-%{version}.tar.bz2

# updated translations
# https://bugzilla.redhat.com/show_bug.cgi?id=575759
Patch0: gcalctool-translations.patch
Patch1: gcalctool-translations2.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: glib2-devel
BuildRequires: gtk2-devel >= 2.6.0
BuildRequires: libglade2-devel
BuildRequires: GConf2-devel
BuildRequires: desktop-file-utils >= 0.9
BuildRequires: scrollkeeper
BuildRequires: gnome-doc-utils
BuildRequires: gettext
BuildRequires: flex
BuildRequires: bison
BuildRequires: intltool

Requires(post): scrollkeeper
Requires(post): GConf2
Requires(postun): scrollkeeper
Requires(preun): GConf2
Requires(pre): GConf2

Requires: GConf2

%description
gcalctool is a powerful graphical calculator with financial, logical and
scientific modes. It uses a multiple precision package to do its arithmetic
to give a high degree of accuracy.

%prep
%setup -q
%patch0 -p1 -b .translations
%patch1 -p2 -b .translations2

%build
%configure --disable-scrollkeeper
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

desktop-file-install --vendor gnome --delete-original	\
  --dir $RPM_BUILD_ROOT%{_datadir}/applications		\
  --remove-only-show-in GNOME				\
  --remove-only-show-in XFCE				\
  $RPM_BUILD_ROOT%{_datadir}/applications/*

# delete this crap
rm -rf $RPM_BUILD_ROOT/var/scrollkeeper

%find_lang gcalctool --with-gnome


%post
scrollkeeper-update -q
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gcalctool.schemas > /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gcalctool.schemas > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gcalctool.schemas > /dev/null || :
fi

%postun
scrollkeeper-update -q


%clean
rm -rf $RPM_BUILD_ROOT


%files -f gcalctool.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_sysconfdir}/gconf/schemas/gcalctool.schemas
%{_bindir}/gcalctool
%{_bindir}/gnome-calculator
%{_datadir}/applications/gnome-gcalctool.desktop
%{_datadir}/gcalctool
%doc %{_mandir}/man1/gcalctool.1.gz


%changelog
* Thu Aug  5 2010 Matthias Clasen <mclasen@redhat.com> - 5.28.2-3
- More translation updates
Resolves: #575759

* Mon May  3 2010 Matthias Clasen <mclasen@redhat.com> - 5.28.2-2
- Update translations
Resolves: #575759

* Mon Jan  4 2010 Matthias Clasen <mclasen@redhat.com> - 5.28.2-1
- Update to 5.28.2, sync to Fedora 12

* Mon Oct 19 2009 Matthias Clasen <mclasen@redhat.com> - 5.28.1-1
- Update to 5.28.1, misc bug fixes

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 5.28.0-1
- Update to 5.28.0

* Mon Sep  7 2009 Matthias Clasen <mclasen@redhat.com> - 5.27.92-1
- Update to 5.27.92

* Tue Aug 25 2009 Matthias Clasen <mclasen@redhat.com> - 5.27.91-1
- Update to 5.27.91

* Tue Aug 11 2009 Matthias Clasen <mclasen@redhat.com> - 5.27.90-1
- Update to 5.27.90

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> - 5.27.5-1
- Update to 5.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Matthias Clasen <mclasen@redhat.com> - 5.27.4-1
- Update to 5.27.4

* Tue Jun 16 2009 Matthias Clasen <mclasen@redhat.com> - 5.27.3-1
- Update to 5.27.3

* Sun May 31 2009 Matthias Clasen <mclasen@redhat.com> - 5.27.2-1
- Update to 5.27.2

* Sat May 16 2009 Matthias Clasen <mclasen@redhat.com> - 5.27.1-1
- Update to 5.27.1

* Sun Apr 12 2009 Matthias Clasen <mclasen@redhat.com> - 5.26.1-1
- Update to 5.26.1

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 5.26.0-1
- Update to 5.26.0

* Tue Mar  3 2009 Matthias Clasen <mclasen@redhat.com> - 5.25.92-1
- Update to 5.25.92

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> - 5.25.91-1
- Update to 5.25.91

* Thu Feb 12 2009 Matthias Clasen <mclasen@redhat.com> - 5.25.90-2
- Properly initialize the type system

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 5.25.90-1
- Update to 5.25.90

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 5.25.5-1
- Update to 2.25.5

* Tue Jan  6 2009 Matthias Clasen <mclasen@redhat.com> - 5.25.4-1
- Update to 5.25.4

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 5.25.3-1
- Update to 5.25.3

* Wed Nov 12 2008 Matthias Clasen <mclasen@redhat.com> - 5.25.1-2
- Update to 5.25.1

* Sun Oct 19 2008 Matthias Clasen <mclasen@redhat.com> - 5.24.1-2
- Update to 5.24.1

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 5.24.0-1
- Update to 5.24.0

* Sun Sep  7 2008 Matthias Clasen <mclasen@redhat.com> - 5.23.92-1
- Update to 5.23.92

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 5.23.91-1
- Update to 5.23.91

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 5.23.90-1
- Update to 5.23.90

* Mon Aug  4 2008 Matthias Clasen <mclasen@redhat.com> - 5.23.6-1
- Update to 5.23.6

* Mon Jul 28 2008 Matthias Clasen <mclasen@redhat.com> - 5.23.5-2
- Use standard icon names

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 5.23.5-1
- Update to 5.23.5

* Tue Jun 17 2008 Matthias Clasen <mclasen@redhat.com> - 5.23.4-1
- Update to 5.23.4

* Wed Jun  4 2008 Matthias Clasen <mclasen@redhat.com> - 5.23.3-1
- Update to 5.23.3

* Tue May 27 2008 Matthias Clasen <mclasen@redhat.com> - 5.23.2-1
- Update to 5.23.2

* Thu Apr 24 2008 Matthias Clasen <mclasen@redhat.com> - 5.23.1-1
- Update to 5.23.1

* Tue Apr  8 2008 Matthias Clasen <mclasen@redhat.com> - 5.22.1-2
- Don't abort on the first keypress

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 5.22.1-1
- Update to 5.22.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 5.22.0-1
- Update to 5.22.0

* Sun Feb 24 2008 Matthias Clasen <mclasen@redhat.com> - 5.21.92-1
- Update to 5.21.92

* Tue Feb 12 2008 Matthias Clasen <mclasen@redhat.com> - 5.21.91-1
- Update to 5.21.91

* Mon Jan 28 2008 Matthias Clasen <mclasen@redhat.com> - 5.21.90-1
- Update to 5.21.90

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 5.21.5-1
- Update 5.21.5

* Tue Dec 18 2007 Matthias Clasen <mclasen@redhat.com> - 5.21.4-1
- Update to 5.21.4

* Wed Dec  5 2007 Matthias Clasen <mclasen@redhat.com> - 5.21.3-1
- Update to 5.21.3

* Mon Nov 12 2007 Matthias Clasen <mclasen@redhat.com> - 5.21.2-1
- Update to 5.21.2

* Mon Nov 12 2007 Matthias Clasen <mclasen@redhat.com> - 5.21.1-1
- Update to 5.21.1

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 5.20.2-1
- 5.20.2 (fix accuracy setting)

* Fri Oct  5 2007 Matthias Clasen <mclasen@redhat.com> - 5.20.1-1
- 5.20.1 (fix XOR in non-arithmetic mode)

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 5.20.0-1
- Update to 5.20.0

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 5.19.92-1
- Update to 5.19.92

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 5.19.90-1
- Update to 5.19.90

* Mon Aug  6 2007 Matthias Clasen <mclasen@redhat.com> - 5.19.6-3
- Use %%find_lang for help files, too

* Thu Aug  2 2007 Matthias Clasen <mclasen@redhat.com> - 5.19.6-2
- Update the License field
- Don't install ChangeLog

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 5.19.6-1
- Update to 5.19.6

* Sun Jul  8 2007 Matthias Clasen <mclasen@redhat.com> - 5.19.5-1
- Update to 5.19.5 

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 5.19.4-1
- Update to 5.19.4

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 5.19.3-1
- Update to 5.19.3

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 5.19.2-1
- Update to 5.19.2

* Wed Mar 28 2007 Matthias Clasen <mclasen@redhat.com> - 5.9.14-2
- Remove OnlyShowIn=GNOME from the desktop file

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 5.9.14-1
- Update to 5.9.14

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 5.9.13-1
- Update to 5.9.13

* Mon Feb 12 2007 Matthias Clasen <mclasen@redhat.com> - 5.9.12-1
- Update to 5.9.12

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 5.9.11-1
- Update to 5.9.11

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 5.9.10-1
- Update to 5.9.10

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 5.9.9-1
- Update to 5.9.9

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 5.9.8-1
- Update to 5.9.8

* Fri Oct 20 2006 Matthias Clasen <mclasen@redhat.com> - 5.9.4-1
- Update to 5.9.4

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 5.8.24-3
- Fix scripts according to packaging guidelines

* Sun Oct  1 2006 Matthias Clasen <mclasen@redhat.com> - 5.8.24-2
- Fix a segfault in the or_IN locale due to careless
  string handling.  (#208695)

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 5.8.24-1.fc6
- Update to 5.8.24

* Sat Aug 18 2006 Matthias Clasen <mclasen@redhat.com> - 5.8.23-1.fc6
- Update to 5.8.23

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> - 5.8.20-1.fc6
- Update to 5.8.20

* Wed Aug  2 2006 Matthias Clasen <mclasen@redhat.com> - 5.8.19-1.fc6
- Update to 5.8.19

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 5.8.17-1
- Update to 5.8.17

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.8.16-2.1
- rebuild

* Mon Jun 12 2006 Matthias Clasen <mclasen@redhat.com> 5.8.16-2
- Update to 5.8.16

* Thu Jun  8 2006 Matthias Clasen <mclasen@redhat.com> 5.8.13-3
- More BuildRequires

* Sun May 21 2006 Matthias Clasen <mclasen@redhat.com> 5.8.13-2
- Add missing BuildRequires  (#191910)

* Tue May 16 2006 Matthias Clasen <mclasen@redhat.com> 5.8.13-1
- Update to 5.8.13

* Tue May  9 2006 Matthias Clasen <mclasen@redhat.com> 5.8.10-1
- Update to 5.8.10

* Wed Apr 26 2006 Matthias Clasen <mclasen@redhat.com> 5.8.9-1
- Update to 5.8.9

* Thu Apr 20 2006 Jesse Keating <jkeating@redhat.com> - 5.7.32-5
- Add postun to clean up gconf schema.

* Wed Apr 19 2006 Jeremy Katz <katzj@redhat.com> - 5.7.32-4
- fix gconf scriptlet

* Mon Apr 17 2006 Matthias Clasen <mclasen@redhat.com> 5.7.32-3
- fix issues pointed out in package review

* Tue Apr 11 2006 Matthias Clasen <mclasen@redhat.com> 5.7.32-2
- initial revision
