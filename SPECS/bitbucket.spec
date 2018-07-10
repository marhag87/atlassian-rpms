Name:           bitbucket
Version:        5.12.0
Release:        1%{?dist}
%define         mysqlconnectorversion 5.1.40
Summary:        A GIT repository web application

License:        Proprietary
URL:            https://www.atlassian.com/software/bitbucket
Source0:        https://www.atlassian.com/software/stash/downloads/binary/atlassian-%{name}-%{version}.tar.gz
Source1:        %{name}.init
Source2:        %{name}-server.xml
Source3:        mysql-connector-java-%{mysqlconnectorversion}-bin.jar
Source4:        %{name}-user.sh
Source5:        %{name}-setenv.sh
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%if 0%{?fedora}
Requires:       java
%else
Requires:       java-1.8.0-oracle
%endif
Requires:       git >= 1.8.0
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

%define bitbucketdatadir %{_datarootdir}/atlassian/%{name}
%define bitbuckethomedir %{_localstatedir}/atlassian/application-data/%{name}
%define bitbucketlogdir  %{_localstatedir}/log/atlassian/%{name}

%description
A GIT repository web application

%prep
%setup -q -n "atlassian-%{name}-%{version}"

%build

%install
install -p -d -m 0755 %{buildroot}%{bitbucketdatadir}
install -p -d -m 0755 %{buildroot}%{bitbuckethomedir}
install -p -d -m 0755 %{buildroot}%{bitbucketlogdir}
install -p -d -m 0755 %{buildroot}%{bitbucketdatadir}/conf/
install -p -d -m 0755 %{buildroot}%{_sysconfdir}/init.d

mv * %{buildroot}%{bitbucketdatadir}/

install -p -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/%{name}
install -p -m 0644 %{SOURCE2} %{buildroot}%{bitbucketdatadir}/conf/server.xml
install -p -m 0644 %{SOURCE3} %{buildroot}%{bitbucketdatadir}/lib/mysql-connector-java-%{mysqlconnectorversion}-bin.jar
install -p -m 0644 %{SOURCE4} %{buildroot}%{bitbucketdatadir}/bin/user.sh
install -p -m 0755 %{SOURCE5} %{buildroot}%{bitbucketdatadir}/bin/setenv.sh

ln -sf %{bitbucketlogdir} %{buildroot}%{bitbucketdatadir}/logs

%clean
rm -rf %{buildroot}

%pre
/etc/init.d/%{name} stop > /dev/null 2>&1
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{bitbuckethomedir} -s /bin/bash \
    -c "Bitbucket user" %{name}
exit 0

%preun
if [ $1 -eq 0 ] ; then
  /etc/init.d/%{name} stop > /dev/null 2>&1
fi

%files
%defattr(-,bitbucket,bitbucket)
%{bitbucketdatadir}
%{bitbuckethomedir}
%{bitbucketlogdir}
%config(noreplace) %{bitbucketdatadir}/conf/server.xml
%config(noreplace) %{bitbucketdatadir}/bin/setenv.sh
%{_sysconfdir}/init.d/%{name}

%changelog
* Wed Jul 11 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.12.0-1
- Update to 5.12.0
* Wed May 30 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.11.1-1
- Update to 5.11.1
* Wed May 16 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.10.1-1
- Update to 5.10.1
* Wed Apr 25 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.10.0-1
- Update to 5.10.0
* Wed Apr 04 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.9.1-1
- Update to 5.9.1
* Wed Mar 21 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.9.0-1
- Update to 5.9.0
* Thu Mar 01 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.8.1-1
- Update to 5.8.1
* Fri Feb 16 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.8.0-1
- Update to 5.8.0
* Wed Jan 31 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.7.1-1
- Update to 5.7.1
* Fri Jan 12 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.7.0-1
- Update to 5.7.0
* Thu Jan 04 2018 Martin Hagstrom <marhag87@gmail.com> 5.6.2-1
- Update to 5.6.2
* Tue Dec 12 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.6.1-1
- Update to 5.6.1
* Tue Dec 05 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.6.0-1
- Update to 5.6.0
* Tue Nov 21 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.5.1-1
- Update to 5.5.1
* Fri Oct 27 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.5.0-1
- Update to 5.5.0
* Wed Oct 11 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.4.1-1
- Update to 5.4.1
* Tue Sep 26 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.4.0-1
- Update to 5.4.0
* Wed Sep 06 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.3.1-1
- Update to 5.3.1
* Thu Aug 17 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.3.0-1
- Update to 5.3.0
* Fri Jul 21 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.2.2-1
- Update to 5.2.2
* Wed Jul 12 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.2.0-1
- Update to 5.2.0
* Thu Jun 08 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.1.0-1
- Update to 5.1.0
* Tue Jun 06 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.0.2-1
- Update to 5.0.2
* Tue May 16 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.0.1-1
- Update to 5.0.1
* Wed Mar 29 2017 Martin Hagstrom (API) <marhag87@gmail.com> 4.14.4-1
- Update to 4.14.4
* Mon Mar 20 2017 Martin Hagstrom (API) <marhag87@gmail.com> 4.14.3-1
- Update to 4.14.3
* Mon Mar 13 2017 Martin Hagstrom (API) <marhag87@gmail.com> 4.14.2-1
- Update to 4.14.2
* Tue Feb 28 2017 Martin Hagstrom (API) <marhag87@gmail.com> 4.14.1-1
- Update to 4.14.1
* Tue Feb 21 2017 Martin Hagstrom <marhag87@gmail.com> 4.14.0-2
- Require java on Fedora
* Tue Feb 21 2017 Martin Hagstrom (API) <marhag87@gmail.com> 4.14.0-1
- Update to 4.14.0
* Tue Jan 24 2017 Martin Hagstrom <marhag87@gmail.com> 4.13.0-2
- Update mysql connector to 5.1.40
* Fri Jan 20 2017 Martin Hagstrom (API) <marhag87@gmail.com> 4.13.0-1
- Update to 4.13.0
* Wed Jan 04 2017 Martin Hagstrom (API) <marhag87@gmail.com> 4.12.1-1
- Update to 4.12.1
* Tue Dec 13 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.12.0-1
- Update to 4.12.0
* Wed Nov 30 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.11.2-1
- Update to 4.11.2
* Thu Nov 17 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.11.1-1
- Update to 4.11.1
* Tue Nov 08 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.11.0-1
- Update to 4.11.0
* Sat Oct 15 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.10.1-1
- Update to 4.10.1
* Wed Oct 05 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.10.0-1
- Update to 4.10.0
* Wed Sep 07 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.9.1-1
- Update to 4.9.1
* Mon Aug 22 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.8.5-1
- Update to 4.8.5
* Wed Aug 17 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.8.4-1
- Update to 4.8.4
* Thu Jul 28 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.8.3-1
- Update to 4.8.3
* Wed Jun 15 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.7.1-1
- Update to 4.7.1
* Thu May 26 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.6.2-1
- Update to 4.6.2
* Tue May 17 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.6.1-1
- Update to 4.6.1
* Thu May 12 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.6.0-1
- Update to 4.6.0
* Wed Apr 13 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.5.2-1
- Update to 4.5.2
* Wed Apr 06 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.5.1-1
- Update to 4.5.1
* Wed Mar 02 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.4.1-1
- Update to 4.4.1
* Tue Mar 01 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.4.0-1
- Update to 4.4.0
* Thu Jan 28 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.3.2-1
- Update to 4.3.2
* Thu Jan 21 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.3.1-1
- Update to 4.3.1
* Tue Jan 12 2016 Martin Hagstrom (API) <marhag87@gmail.com> 4.3.0-1
- Update to 4.3.0
* Sat Dec 19 2015 Martin Hagstrom <marhag87@gmail.com> 4.2.0-3
- Don't get osgi provides and requires
* Sat Dec 19 2015 Martin Hagstrom <marhag87@gmail.com> 4.2.0-2
- Don't build debug package
* Fri Dec 11 2015 Martin Hagstrom <marhag87@gmail.com> 4.2.0-1
- Initial release
