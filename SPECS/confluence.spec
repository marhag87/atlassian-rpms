Name:           confluence
Version:        5.10.3
%define         mysqlconnectorversion 5.1.39
Release:        2%{?dist}
Summary:        A team collaboration web application

License:        Proprietary
URL:            https://www.atlassian.com/software/confluence
Source0:        https://www.atlassian.com/software/confluence/downloads/binary/atlassian-%{name}-%{version}.tar.gz
Source1:        %{name}.init
Source2:        %{name}-init.properties
Source3:        %{name}-server.xml
Source4:        mysql-connector-java-%{mysqlconnectorversion}-bin.jar
Source5:        %{name}-user.sh
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires:       java-1.8.0-oracle
Requires(pre):  shadow-utils

# Don't repackage jar files
%define __jar_repack %{nil}

# Don't get osgi provides and requires
%define __osgi_provides %{nil}
%define __osgi_requires %{nil}
%define __osgi_provides_opts %{nil}
%define __osgi_requires_opts %{nil}

# Don't build debug package
%define debug_package %{nil}

%define confluencedatadir %{_datarootdir}/atlassian/%{name}
%define confluencehomedir %{_localstatedir}/atlassian/application-data/%{name}
%define confluencelogdir  %{_localstatedir}/log/atlassian/%{name}

%description
A team collaboration web application

%prep
%setup -q -n "atlassian-%{name}-%{version}"

%build

%install
install -p -d -m 0755 %{buildroot}%{confluencedatadir}
install -p -d -m 0755 %{buildroot}%{confluencehomedir}
install -p -d -m 0755 %{buildroot}%{confluencelogdir}
install -p -d -m 0755 %{buildroot}%{_sysconfdir}/init.d

mv * %{buildroot}%{confluencedatadir}/

install -p -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/%{name}
install -p -m 0644 %{SOURCE2} %{buildroot}%{confluencedatadir}/%{name}/WEB-INF/classes/%{name}-init.properties
install -p -m 0644 %{SOURCE3} %{buildroot}%{confluencedatadir}/conf/server.xml
install -p -m 0644 %{SOURCE4} %{buildroot}%{confluencedatadir}/%{name}/WEB-INF/lib/mysql-connector-java-%{mysqlconnectorversion}-bin.jar
install -p -m 0644 %{SOURCE5} %{buildroot}%{confluencedatadir}/bin/user.sh

rmdir %{buildroot}%{confluencedatadir}/logs
ln -sf %{confluencelogdir} %{buildroot}%{confluencedatadir}/logs

%clean
rm -rf %{buildroot}

%pre
/etc/init.d/%{name} stop > /dev/null 2>&1
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{confluencehomedir} -s /bin/bash \
    -c "Confluence user" %{name}
exit 0

%preun
if [ $1 -eq 0 ] ; then
  /etc/init.d/%{name} stop > /dev/null 2>&1
fi

%files
%defattr(-,confluence,confluence)
%{confluencedatadir}
%{confluencehomedir}
%{confluencelogdir}
%config(noreplace) %{confluencedatadir}/%{name}/WEB-INF/classes/%{name}-init.properties
%config(noreplace) %{confluencedatadir}/conf/server.xml
%config(noreplace) %{confluencedatadir}/bin/setenv.sh
%{_sysconfdir}/init.d/%{name}

%changelog
* Tue Aug 09 2016 Martin Hagstrom <martin.hagstrom@ericsson.com> 5.10.3-2
- Update mysql connector to 5.1.39
* Mon Aug 01 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.10.3-1
- Update to 5.10.3
* Fri Jul 01 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.10.1-1
- Update to 5.10.1
* Wed Jun 08 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.10.0-1
- Update to 5.10.0
* Mon Jun 06 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.9.12-1
- Update to 5.9.12
* Fri May 20 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.9.11-1
- Update to 5.9.11
* Thu May 05 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.9.10-1
- Update to 5.9.10
* Fri Apr 22 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.9.9-1
- Update to 5.9.9
* Tue Apr 12 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.9.8-1
- Update to 5.9.8
* Thu Mar 17 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.9.7-1
- Update to 5.9.7
* Thu Mar 03 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.9.6-1
- Update to 5.9.6
* Mon Feb 15 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.9.5-1
- Update to 5.9.5
* Mon Jan 11 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.9.4-1
- Update to 5.9.4
* Wed Dec 30 2015 Martin Hagstrom (API) <marhag87@gmail.com> 5.9.3-1
- Update to 5.9.3
* Sat Dec 19 2015 Martin Hagstrom <marhag87@gmail.com> 5.9.2-3
- Don't get osgi provides and requires
* Sat Dec 19 2015 Martin Hagstrom <marhag87@gmail.com> 5.9.2-2
- Don't build debug package
* Fri Dec 11 2015 Martin Hagstrom <marhag87@gmail.com> 5.9.2-1
- Initial release
