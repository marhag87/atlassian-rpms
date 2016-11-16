Name:           jira
Version:        7.2.5
Release:        1%{?dist}
Summary:        An issue tracking web application

License:        Proprietary
URL:            https://www.atlassian.com/software/jira
Source0:        https://www.atlassian.com/software/jira/downloads/binary/atlassian-%{name}-software-%{version}-%{name}-%{version}.tar.gz#/atlassian-%{name}-%{version}.tar.gz
Source1:        %{name}.init
Source2:        %{name}-application.properties
Source3:        %{name}-server.xml
Source4:        mysql-connector-java-5.1.37-bin.jar
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

%define jiradatadir %{_datarootdir}/atlassian/%{name}
%define jirahomedir %{_localstatedir}/atlassian/application-data/%{name}
%define jiralogdir  %{_localstatedir}/log/atlassian/%{name}

%description
An issue tracking web application

%prep
%setup -q -n "atlassian-%{name}-software-%{version}-standalone"

%build

%install
install -p -d -m 0755 %{buildroot}%{jiradatadir}
install -p -d -m 0755 %{buildroot}%{jirahomedir}
install -p -d -m 0755 %{buildroot}%{jiralogdir}
install -p -d -m 0755 %{buildroot}%{_sysconfdir}/init.d

mv * %{buildroot}%{jiradatadir}/

install -p -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/%{name}
install -p -m 0644 %{SOURCE2} %{buildroot}%{jiradatadir}/atlassian-%{name}/WEB-INF/classes/%{name}-application.properties
install -p -m 0644 %{SOURCE3} %{buildroot}%{jiradatadir}/conf/server.xml
install -p -m 0644 %{SOURCE4} %{buildroot}%{jiradatadir}/lib/mysql-connector-java-5.1.37-bin.jar
install -p -m 0644 %{SOURCE5} %{buildroot}%{jiradatadir}/bin/user.sh

rmdir %{buildroot}%{jiradatadir}/logs
ln -sf %{jiralogdir} %{buildroot}%{jiradatadir}/logs

%clean
rm -rf %{buildroot}

%pre
/etc/init.d/%{name} stop > /dev/null 2>&1
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{jirahomedir} -s /bin/bash \
    -c "Jira user" %{name}
exit 0

%preun
if [ $1 -eq 0 ] ; then
  /etc/init.d/%{name} stop > /dev/null 2>&1 || true
fi

%files
%defattr(-,jira,jira)
%{jiradatadir}
%{jirahomedir}
%{jiralogdir}
%config(noreplace) %{jiradatadir}/atlassian-%{name}/WEB-INF/classes/%{name}-application.properties
%config(noreplace) %{jiradatadir}/conf/server.xml
%config(noreplace) %{jiradatadir}/bin/setenv.sh
%{_sysconfdir}/init.d/%{name}

%changelog
* Wed Nov 16 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.2.5-1
- Update to 7.2.5
* Wed Nov 02 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.2.4-1
- Update to 7.2.4
* Sat Oct 15 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.2.3-1
- Update to 7.2.3
* Tue Sep 27 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.2.2-1
- Update to 7.2.2
* Wed Sep 07 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.2.1-1
- Update to 7.2.1
* Thu Aug 25 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.2.0-1
- Update to 7.2.0
* Sun Jul 10 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.1.9-1
- Update to 7.1.9
* Mon Jun 20 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.1.8-1
- Update to 7.1.8
* Wed May 18 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.1.7-1
- Update to 7.1.7
* Wed May 04 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.1.6-1
- Update to 7.1.6
* Wed Apr 06 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.1.4-1
- Update to 7.1.4
* Wed Mar 16 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.1.2-1
- Update to 7.1.2
* Mon Mar 14 2016 Martin Hagstrom <martin.hagstrom@ericsson.com> 7.1.1-2
- Allow failing service stop at uninstall
* Wed Mar 02 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.1.1-1
- Update to 7.1.1
* Thu Feb 11 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.1.0-1
- Update to 7.1.0
* Thu Jan 28 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.0.10-1
- Update to 7.0.10
* Wed Jan 20 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.0.9-1
- Update to 7.0.9
* Sun Dec 20 2015 Martin Hagstrom <marhag87@gmail.com> 7.0.5-3
- Change source name to better comply with other atlassian products
* Sat Dec 19 2015 Martin Hagstrom <marhag87@gmail.com> 7.0.5-2
- Don't get osgi provides and requires
* Sat Dec 19 2015 Martin Hagstrom (API) <marhag87@gmail.com> 7.0.5-1
- Update to 7.0.5
* Sat Dec 19 2015 Martin Hagstrom <marhag87@gmail.com> 7.0.4-2
- Don't build debug package
* Fri Dec 11 2015 Martin Hagstrom <marhag87@gmail.com> 7.0.4-1
- Initial release
