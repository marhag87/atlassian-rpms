Name:           bitbucket
Version:        5.16.0
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
Source6:        %{name}.service

Requires:       java >= 1.8.0

BuildRequires:  systemd

Requires(pre):  	shadow-utils
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd

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
%define bitbucketworkdir %{_localstatedir}/cache/atlassian/%{name}/work
%define bitbuckettempdir %{_localstatedir}/cache/atlassian/%{name}/temp

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
install -p -d -m 0755 %{buildroot}%{bitbucketworkdir}
install -p -d -m 0755 %{buildroot}%{bitbuckettempdir}

mv * %{buildroot}%{bitbucketdatadir}/

install -p -m 0644 %{SOURCE2} %{buildroot}%{bitbucketdatadir}/conf/server.xml
install -p -m 0644 %{SOURCE3} %{buildroot}%{bitbucketdatadir}/lib/mysql-connector-java-%{mysqlconnectorversion}-bin.jar
install -p -m 0644 %{SOURCE4} %{buildroot}%{bitbucketdatadir}/bin/user.sh
install -p -m 0755 %{SOURCE5} %{buildroot}%{bitbucketdatadir}/bin/setenv.sh
install -D -p -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/%{name}.service

#rmdir %{buildroot}%{bitbucketdatadir}/logs
#rmdir %{buildroot}%{bitbucketdatadir}/work
rm -rf %{buildroot}%{bitbucketdatadir}/temp

ln -sf %{bitbucketlogdir}  %{buildroot}%{bitbucketdatadir}/logs
ln -sf %{bitbucketworkdir} %{buildroot}%{bitbucketdatadir}/work
ln -sf %{bitbuckettempdir} %{buildroot}%{bitbucketdatadir}/temp

%clean
rm -rf %{buildroot}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{bitbuckethomedir} -s /bin/bash \
    -c "%{name} user" %{name}
exit 0

%files
%defattr(-,root,root)
%{bitbucketdatadir}
%attr(-,bitbucket,bitbucket) %{bitbuckethomedir}
%attr(-,bitbucket,bitbucket) %{bitbucketlogdir}
%attr(-,bitbucket,bitbucket) %{bitbucketworkdir}
%attr(-,bitbucket,bitbucket) %{bitbuckettempdir}
%config(noreplace) %{bitbucketdatadir}/conf/server.xml
%config(noreplace) %{bitbucketdatadir}/bin/setenv.sh
%{_unitdir}/%{name}.service

%changelog
* Wed Nov 21 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.16.0-1
- Update to 5.16.0
* Thu Nov 15 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.15.1-1
- Update to 5.15.1
* Fri Oct 19 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.15.0-1
- Update to 5.15.0
* Sat Sep 29 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.14.1-1
- Update to 5.14.1
* Fri Sep 28 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.13.3-1
- Update to 5.13.3
* Wed Sep 12 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.14.0-1
- Update to 5.14.0
* Thu Aug 23 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.13.1-1
- Update to 5.13.1
* Wed Aug 08 2018 Martin Hagstrom (API) <marhag87@gmail.com> 5.13.0-1
- Update to 5.13.0
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
