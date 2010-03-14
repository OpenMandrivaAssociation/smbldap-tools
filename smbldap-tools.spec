Summary:	User & Group administration tools for Samba-OpenLDAP
Name: 		smbldap-tools
Version: 	0.9.5
Release: 	%mkrel 6
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
