Name:           jira
Version:        7.10.2
Release:        1%{?dist}
%define         mysqlconnectorversion 5.1.40
Summary:        An issue tracking web application

License:        Proprietary
URL:            https://www.atlassian.com/software/jira
Source0:        https://www.atlassian.com/software/jira/downloads/binary/atlassian-%{name}-software-%{version}-%{name}-%{version}.tar.gz#/atlassian-%{name}-%{version}.tar.gz
Source1:        %{name}.service
Source2:        %{name}-application.properties
Source3:        %{name}-server.xml
Source4:        mysql-connector-java-%{mysqlconnectorversion}-bin.jar
Source5:        %{name}-user.sh
Source6:        %{name}-check-java.sh
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%if 0%{?fedora}
Requires:       java
%else
%if 0%{?centos}
Requires:       java-1.8.0
%else
Requires:       java-1.8.0-oracle
%endif
%endif
Requires(pre):  shadow-utils
Requires:       systemd

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
install -p -d -m 0755 %{buildroot}%{_unitdir}

mv * %{buildroot}%{jiradatadir}/

install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -m 0644 %{SOURCE2} %{buildroot}%{jiradatadir}/atlassian-%{name}/WEB-INF/classes/%{name}-application.properties
install -p -m 0644 %{SOURCE3} %{buildroot}%{jiradatadir}/conf/server.xml
install -p -m 0644 %{SOURCE4} %{buildroot}%{jiradatadir}/lib/mysql-connector-java-%{mysqlconnectorversion}-bin.jar
install -p -m 0644 %{SOURCE5} %{buildroot}%{jiradatadir}/bin/user.sh
install -p -m 0755 %{SOURCE6} %{buildroot}%{jiradatadir}/bin/check-java.sh

rmdir %{buildroot}%{jiradatadir}/logs
ln -sf %{jiralogdir} %{buildroot}%{jiradatadir}/logs

%clean
rm -rf %{buildroot}

%pre
service %{name} stop > /dev/null 2>&1
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{jirahomedir} -s /bin/bash \
    -c "Jira user" %{name}
exit 0

%preun
if [ $1 -eq 0 ] ; then
  service %{name} stop > /dev/null 2>&1 || true
fi

%files
%defattr(-,jira,jira)
%{jiradatadir}
%{jirahomedir}
%{jiralogdir}
%config(noreplace) %{jiradatadir}/atlassian-%{name}/WEB-INF/classes/%{name}-application.properties
%config(noreplace) %{jiradatadir}/conf/server.xml
%config(noreplace) %{jiradatadir}/bin/setenv.sh
%{_unitdir}/%{name}.service

%changelog
* Thu Jun 28 2018 Martin Hagstrom (API) <marhag87@gmail.com> 7.10.2-1
- Update to 7.10.2
* Thu Jun 14 2018 Martin Hagstrom (API) <marhag87@gmail.com> 7.10.1-1
- Update to 7.10.1
* Wed May 30 2018 Martin Hagstrom (API) <marhag87@gmail.com> 7.10.0-1
- Update to 7.10.0
* Thu May 10 2018 Martin Hagstrom (API) <marhag87@gmail.com> 7.9.2-1
- Update to 7.9.2
* Tue May 08 2018 Martin Hagstrom (API) <marhag87@gmail.com> 7.9.0-1
- Update to 7.9.0
* Wed Apr 25 2018 Martin Hagstrom (API) <marhag87@gmail.com> 7.9.1-1
- Update to 7.9.1
* Mon Apr 23 2018 Martin Hagstrom (API) <marhag87@gmail.com> 7.9.0-1
- Update to 7.9.0
* Wed Apr 04 2018 Martin Hagstrom (API) <marhag87@gmail.com> 7.8.2-1
- Update to 7.8.2
* Tue Mar 20 2018 Martin Hagstrom (API) <marhag87@gmail.com> 7.8.1-1
- Update to 7.8.1
* Wed Feb 21 2018 Martin Hagstrom (API) <marhag87@gmail.com> 7.8.0-1
- Update to 7.8.0
* Thu Feb 01 2018 Martin Hagstrom (API) <marhag87@gmail.com> 7.7.1-1
- Update to 7.7.1
* Fri Jan 12 2018 Martin Hagstrom (API) <marhag87@gmail.com> 7.7.0-1
- Update to 7.7.0
* Wed Jan 10 2018 Martin Hagstrom (API) <marhag87@gmail.com> 7.6.3-1
- Update to 7.6.3
* Thu Jan 04 2018 Martin Hagstrom (API) <marhag87@gmail.com> 7.6.2-1
- Update to 7.6.2
* Mon Dec 18 2017 Martin Hagstrom <marhag87@gmail.com> 7.6.1-2
- Systemd service file should not be executable
* Thu Dec 07 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.6.1-1
- Update to 7.6.1
* Tue Dec 05 2017 Martin Hagstrom <marhag87@gmail.com> 7.6.0-2
- Use systemd
* Thu Nov 16 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.6.0-1
- Update to 7.6.0
* Thu Nov 16 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.5.3-1
- Update to 7.5.3
* Wed Nov 01 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.5.2-1
- Update to 7.5.2
* Thu Oct 26 2017 Martin Hagstrom <marhag87@gmail.com> 7.5.1-2
- Allow OpenJDK java
* Tue Oct 17 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.5.1-1
- Update to 7.5.1
* Thu Sep 07 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.5.0-1
- Update to 7.5.0
* Tue Sep 05 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.4.4-1
- Update to 7.4.4
* Wed Aug 23 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.4.3-1
- Update to 7.4.3
* Sat Aug 05 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.4.2-1
- Update to 7.4.2
* Thu Jul 13 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.4.1-1
- Update to 7.4.1
* Fri Jun 30 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.4.0-1
- Update to 7.4.0
* Tue Jun 20 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.3.8-1
- Update to 7.3.8
* Tue Jun 06 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.3.7-1
- Update to 7.3.7
* Fri Apr 28 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.3.6-1
- Update to 7.3.6
* Wed Apr 19 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.3.5-1
- Update to 7.3.5
* Tue Apr 04 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.3.4-1
- Update to 7.3.4
* Tue Mar 14 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.3.3-1
- Update to 7.3.3
* Wed Mar 01 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.3.2-1
- Update to 7.3.2
* Tue Feb 21 2017 Martin Hagstrom <marhag87@gmail.com> 7.3.1-2
- Require java on Fedora
* Mon Feb 06 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.3.1-1
- Update to 7.3.1
* Tue Jan 24 2017 Martin Hagstrom <marhag87@gmail.com> 7.3.0-2
- Update mysql connector to 5.1.40
* Tue Jan 03 2017 Martin Hagstrom (API) <marhag87@gmail.com> 7.3.0-1
- Update to 7.3.0
* Thu Dec 29 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.2.7-1
- Update to 7.2.7
* Wed Dec 07 2016 Martin Hagstrom (API) <marhag87@gmail.com> 7.2.6-1
- Update to 7.2.6
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
