# THIS PACKAGE IS IN SVN
# PLEASE DO NOT UPLOAD WITHOUT COMMITING
# YOUR CHANGES

Summary:	User & Group administration tools for Samba-OpenLDAP
Name: 		smbldap-tools
Version: 	0.9.2
Release: 	%mkrel 2
Group: 		System/Servers
License: 	GPL
URL:		http://samba.IDEALX.org/
Source0: 	http://samba.idealx.org/dist/smbldap-tools-%{version}.tar.bz2
Source1: 	mkntpwd.tar.bz2
Patch:		smbldap-tools-0.9.1-mdkconfig.patch
# http://qa.mandriva.com/show_bug.cgi?id=23921
Patch1:		smbldap-tools-0.9.2-accountOC.patch
Requires:	perl-IO-Socket-SSL
BuildRoot:	%{_tmppath}/%{name}-%{version}

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
%patch -p1 -b .mdkconf
%patch1 -p1

%build

pushd mkntpwd
%make CFLAGS="%{optflags}"
popd

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/smbldap-tools
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{perl_vendorlib}

install -m0644 smbldap.conf %{buildroot}%{_sysconfdir}/smbldap-tools/
install -m0644 smbldap_bind.conf %{buildroot}%{_sysconfdir}/smbldap-tools/
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CONTRIBUTORS COPYING ChangeLog INFRA INSTALL README TODO doc
%doc smb.conf smbldap.conf smbldap_bind.conf configure.pl
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap.conf
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap_bind.conf
%attr(0755,root,root) %{_sbindir}/mkntpwd
%attr(0755,root,root) %{_sbindir}/smbldap-groupadd
%attr(0755,root,root) %{_sbindir}/smbldap-groupdel
%attr(0755,root,root) %{_sbindir}/smbldap-groupmod
%attr(0755,root,root) %{_sbindir}/smbldap-groupshow
%attr(0755,root,root) %{_sbindir}/smbldap-passwd
%attr(0755,root,root) %{_sbindir}/smbldap-populate
%attr(0755,root,root) %{_sbindir}/smbldap-useradd
%attr(0755,root,root) %{_sbindir}/smbldap-userdel
%attr(0755,root,root) %{_sbindir}/smbldap-usermod
%attr(0755,root,root) %{_sbindir}/smbldap-userinfo
%attr(0755,root,root) %{_sbindir}/smbldap-usershow
%attr(0644,root,root) %{perl_vendorlib}/smbldap_tools.pm



