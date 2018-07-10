Summary:	User & Group administration tools for Samba-OpenLDAP
Name: 		smbldap-tools
Version: 	0.9.5
Release: 	17
Group: 		System/Servers
License: 	GPL
URL:		https://gna.org/projects/smbldap-tools/
Source0: 	http://download.gna.org/smbldap-tools/packages/%{name}-%{version}.tgz
Source1: 	mkntpwd.tar.bz2
Patch0:		smbldap-tools-mdvconfig.diff
Patch1:		smbldap-tools-utf-8.patch
Requires:	perl-IO-Socket-SSL
BuildRequires:	perl-doc
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Smbldap-tools is a set of perl scripts written by Idealx. Those scripts are
designed to help managing users and groups in a ldap directory server and
can be used both by users and administrators of Linux systems:
. users can change their password in a way similar to the standard
  "passwd" command,
. administrators can perform users and groups management

Scripts are described in the Smbldap-tools User Manual
(http://samba.idealx.org/smbldap-tools.en.html) which also give command
line examples.
You can download the latest version on Idealx web site
(http://samba.idealx.org/dist/).
Comments and/or questions can be sent to the smbldap-tools mailing list
(http://lists.idealx.org/lists/samba).

%prep

%setup -q -a1
%patch0 -p0 -b .mdvconf
%patch1 -p1 -b .utf8

# nuke that IDEALX stuff from the code
for i in `find -type f`; do
    perl -pi -e "s|/etc/opt/IDEALX/smbldap-tools/|%{_sysconfdir}/smbldap-tools/|g; \
    s|/opt/IDEALX/bin:||g; \
    s|/opt/IDEALX/sbin|%{_sbindir}|g" $i
done

%build
%serverbuild

pushd mkntpwd
%make CFLAGS="$CFLAGS"
popd

# make some manpages
for i in smbldap-groupadd smbldap-groupdel smbldap-groupmod smbldap-groupshow smbldap-passwd \
    smbldap-populate smbldap-useradd smbldap-userdel smbldap-userinfo smbldap-usermod smbldap-usershow; do
    perldoc $i > $i.1
done

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/smbldap-tools
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{perl_vendorlib}
install -d %{buildroot}%{_mandir}/man1

install -m0644 smbldap.conf %{buildroot}%{_sysconfdir}/smbldap-tools/
install -m0600 smbldap_bind.conf %{buildroot}%{_sysconfdir}/smbldap-tools/
install -m0644 smbldap_tools.pm %{buildroot}%{perl_vendorlib}/

install -m0755 smbldap-groupadd %{buildroot}%{_sbindir}/
install -m0755 smbldap-groupdel %{buildroot}%{_sbindir}/
install -m0755 smbldap-groupmod %{buildroot}%{_sbindir}/
install -m0755 smbldap-groupshow %{buildroot}%{_sbindir}/
install -m0755 smbldap-passwd %{buildroot}%{_sbindir}/
install -m0755 smbldap-populate %{buildroot}%{_sbindir}/
install -m0755 smbldap-useradd %{buildroot}%{_sbindir}/
install -m0755 smbldap-userdel %{buildroot}%{_sbindir}/
install -m0755 smbldap-userinfo %{buildroot}%{_sbindir}/
install -m0755 smbldap-usermod %{buildroot}%{_sbindir}/
install -m0755 smbldap-usershow %{buildroot}%{_sbindir}/
install -m0755 mkntpwd/mkntpwd %{buildroot}%{_sbindir}/
install -m0644 smbldap-*.1 %{buildroot}%{_mandir}/man1/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CONTRIBUTORS COPYING ChangeLog INFRA INSTALL README TODO doc
%doc smbldap.conf smbldap_bind.conf configure.pl
%dir %{_sysconfdir}/smbldap-tools
%config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap.conf
%config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap_bind.conf
%{_sbindir}/*
%{perl_vendorlib}/smbldap_tools.pm
%{_mandir}/man1/*


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.5-7mdv2011.0
+ Revision: 669991
- mass rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.5-6mdv2010.1
+ Revision: 519071
- rebuild

* Tue Oct 06 2009 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 0.9.5-5mdv2010.0
+ Revision: 454903
- P1: utf8 support

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.9.5-4mdv2010.0
+ Revision: 427198
- rebuild

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0.9.5-3mdv2009.0
+ Revision: 265708
- rebuild early 2009.0 package (before pixel changes)

* Tue Apr 29 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0.9.5-2mdv2009.0
+ Revision: 198994
- own configuration directory, and clean up files section

* Tue Apr 22 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.5-1mdv2009.0
+ Revision: 196511
- 0.9.5
- rediffed P0

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Nov 12 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.9.4-1mdv2008.1
+ Revision: 108348
- new version
  rediff patch 0
  drop patches 1 and 2, merged upstream

* Wed Aug 01 2007 Andreas Hasenack <andreas@mandriva.com> 0.9.2-4mdv2008.0
+ Revision: 57798
- use userCN for display name attribute: it contains the
  accented characters of the user name, if any (and gecos,
  which was being used before, doesn't)

* Mon Jul 09 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-3mdv2008.0
+ Revision: 50633
- fix url (idealx is gone?)
- add some man pages and add build deps for it (perl-doc)
- fix some annoying referals to /opt/idealx in some files


* Wed Jul 26 2006 Andreas Hasenack <andreas@mandriva.com> 0.9.2-2mdv2007.0
+ Revision: 42099
- using "account" instead of "inetOrgPerson" for the structural
  objectClass for computer accounts (#23921)
- import smbldap-tools-0.9.2-1mdk

* Thu Jan 12 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-1mdk
- 0.9.2

* Tue Oct 25 2005 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-3mdk
- fix #19316

* Mon Sep 19 2005 Buchan Milne <bgmilne@mandriva.org> 0.9.1-2mdk
- reapply changes as when shipped with samba to match our default smb.conf,
  LDAP layout, OpenLDAP ACLs, and default nss_ldap behaviour.

* Wed Jun 22 2005 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-1mdk
- 0.9.1
- nuke redundant P0

* Thu Apr 21 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.8.8-1mdk
- 0.8.8
- use the macromdv2007.1- rediff P0

* Thu Feb 17 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.8.7-5mdk
- nuke compat softlinks

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.8.7-4mdk
- provide compat softlinks

* Tue Feb 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.8.7-3mdk
- provide mkntpwd (from older smbldap-tools source)

* Tue Feb 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.8.7-2mdk
- put the *.pm file in /usr/lib/perl5/vendor_perl/5.8.8/ (buchan)

* Mon Feb 14 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.8.7-1mdk
- initial Mandrakelinux package
- used parts of the provided spec file
- added P0

