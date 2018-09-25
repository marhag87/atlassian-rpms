Name:           confluence
Version:        6.11.2
Release:        1%{?dist}
%define         mysqlconnectorversion 5.1.40
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

%if 0%{?fedora}
Requires:       java
%else
Requires:       java-1.8.0-oracle
%endif
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
* Wed Sep 26 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.11.2-1
- Update to 6.11.2
* Tue Sep 11 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.11.1-1
- Update to 6.11.1
* Wed Aug 15 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.11.0-1
- Update to 6.11.0
* Tue Aug 14 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.10.2-1
- Update to 6.10.2
* Wed Jul 18 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.10.1-1
- Update to 6.10.1
* Wed Jun 27 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.10.0-1
- Update to 6.10.0
* Tue Jun 05 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.9.1-1
- Update to 6.9.1
* Wed May 09 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.9.0-1
- Update to 6.9.0
* Fri Apr 27 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.8.2-1
- Update to 6.8.2
* Thu Apr 05 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.8.1-1
- Update to 6.8.1
* Thu Mar 22 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.8.0-1
- Update to 6.8.0
* Tue Mar 06 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.7.2-1
- Update to 6.7.2
* Tue Feb 13 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.7.1-1
- Update to 6.7.1
* Wed Jan 31 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.7.0-1
- Update to 6.7.0
* Wed Jan 24 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.6.2-1
- Update to 6.6.2
* Tue Jan 09 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.6.1-1
- Update to 6.6.1
* Tue Dec 12 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.6.0-1
- Update to 6.6.0
* Tue Dec 05 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.5.2-1
- Update to 6.5.2
* Tue Nov 21 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.5.1-1
- Update to 6.5.1
* Thu Nov 02 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.5.0-1
- Update to 6.5.0
* Fri Oct 27 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.4.3-1
- Update to 6.4.3
* Wed Oct 11 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.4.2-1
- Update to 6.4.2
* Tue Sep 26 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.4.1-1
- Update to 6.4.1
* Thu Sep 07 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.4.0-1
- Update to 6.4.0
* Wed Sep 06 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.3.4-1
- Update to 6.3.4
* Thu Aug 17 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.3.3-1
- Update to 6.3.3
* Sat Aug 05 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.3.2-1
- Update to 6.3.2
* Thu Jul 13 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.3.1-1
- Update to 6.3.1
* Wed Jul 12 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.2.4-1
- Update to 6.2.4
* Thu Jun 22 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.2.3-1
- Update to 6.2.3
* Wed Jun 14 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.2.2-1
- Update to 6.2.2
* Tue May 30 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.2.1-1
- Update to 6.2.1
* Tue May 16 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.2.0-1
- Update to 6.2.0
* Wed May 03 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.1.3-1
- Update to 6.1.3
* Wed Apr 19 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.1.2-1
- Update to 6.1.2
* Sun Apr 09 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.1.1-1
- Update to 6.1.1
* Fri Apr 07 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.0.7-1
- Update to 6.0.7
* Mon Apr 03 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.1.1-1
- Update to 6.1.1
* Mon Mar 20 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.1.0-1
- Update to 6.1.0
* Fri Mar 17 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.0.7-1
- Update to 6.0.7
* Wed Feb 22 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.0.6-1
- Update to 6.0.6
* Tue Feb 21 2017 Martin Hagstrom <marhag87@gmail.com> 6.0.5-2
- Require java on Fedora
* Mon Feb 06 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.0.5-1
- Update to 6.0.5
* Tue Jan 24 2017 Martin Hagstrom <marhag87@gmail.com> 6.0.4-3
- Update mysql connector to 5.1.40
* Tue Jan 17 2017 Martin Hagstrom <marhag87@gmail.com> 6.0.4-2
- Update server.xml to 6.0 standard, removes https config
* Tue Jan 17 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.0.4-1
- Update to 6.0.4
* Mon Dec 19 2016 Martin Hagstrom (API) <marhag87@gmail.com> 6.0.3-1
- Update to 6.0.3
* Thu Oct 20 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.10.8-1
- Update to 5.10.8
* Fri Sep 30 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.10.7-1
- Update to 5.10.7
* Mon Sep 26 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.10.6-1
- Update to 5.10.6
* Mon Aug 22 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.10.4-1
- Update to 5.10.4
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
