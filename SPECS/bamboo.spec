Name:           bamboo
Version:        6.7.2
Release:        1%{?dist}
%define         mysqlconnectorversion 5.1.40
Summary:        A continuous integration web application

License:        Proprietary
URL:            https://www.atlassian.com/software/bamboo
Source0:        https://www.atlassian.com/software/bamboo/downloads/binary/atlassian-%{name}-%{version}.tar.gz
Source1:        %{name}.service
Source2:        %{name}-server.xml
Source3:        mysql-connector-java-%{mysqlconnectorversion}-bin.jar
Source4:        %{name}-init.properties
Source5:        stop-%{name}.sh
Source6:        %{name}-setenv.sh

Requires:       java >= 1.8.0

BuildRequires:  systemd

Requires(pre):  	shadow-utils
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd

AutoReqProv:    no

# Don't repackage jar files
%define __jar_repack %{nil}

# Don't get osgi provides and requires
%define __osgi_provides %{nil}
%define __osgi_requires %{nil}
%define __osgi_provides_opts %{nil}
%define __osgi_requires_opts %{nil}

# Don't build debug package
%define debug_package %{nil}

%define bamboodatadir %{_datarootdir}/atlassian/%{name}
%define bamboohomedir %{_localstatedir}/atlassian/application-data/%{name}
%define bamboologdir  %{_localstatedir}/log/atlassian/%{name}
%define bambooworkdir %{_localstatedir}/cache/atlassian/%{name}/work
%define bambootempdir %{_localstatedir}/cache/atlassian/%{name}/temp

%description
A continuous integration web application

%prep
%setup -q -n "atlassian-%{name}-%{version}"

%build

%install
install -p -d -m 0755 %{buildroot}%{bamboodatadir}
install -p -d -m 0755 %{buildroot}%{bamboohomedir}
install -p -d -m 0755 %{buildroot}%{bamboologdir}
install -p -d -m 0755 %{buildroot}%{bambooworkdir}
install -p -d -m 0755 %{buildroot}%{bambootempdir}
install -p -d -m 0755 %{buildroot}%{_unitdir}

mv * %{buildroot}%{bamboodatadir}/

install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -m 0644 %{SOURCE2} %{buildroot}%{bamboodatadir}/conf/server.xml
install -p -m 0644 %{SOURCE3} %{buildroot}%{bamboodatadir}/lib/mysql-connector-java-%{mysqlconnectorversion}-bin.jar
install -p -m 0644 %{SOURCE4} %{buildroot}%{bamboodatadir}/atlassian-%{name}/WEB-INF/classes/%{name}-init.properties
install -p -m 0755 %{SOURCE5} %{buildroot}%{bamboodatadir}/bin/stop-%{name}.sh
install -p -m 0755 %{SOURCE6} %{buildroot}%{bamboodatadir}/bin/setenv.sh

rmdir %{buildroot}%{bamboodatadir}/logs
rmdir %{buildroot}%{bamboodatadir}/work
rm -rf %{buildroot}%{bamboodatadir}/temp

ln -sf %{bamboologdir}  %{buildroot}%{bamboodatadir}/logs
ln -sf %{bambooworkdir} %{buildroot}%{bamboodatadir}/work
ln -sf %{bambootempdir} %{buildroot}%{bamboodatadir}/temp

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
    useradd -r -g %{name} -d %{bamboohomedir} -s /bin/bash \
    -c "%{name} user" %{name}
exit 0

%files
%defattr(-,root,root)
%{bamboodatadir}
%attr(-,bamboo,bamboo) %{bamboohomedir}
%attr(-,bamboo,bamboo) %{bamboologdir}
%attr(-,bamboo,bamboo) %{bambooworkdir}
%attr(-,bamboo,bamboo) %{bambootempdir}

%config(noreplace) %{bamboodatadir}/conf/server.xml
%config(noreplace) %{bamboodatadir}/bin/setenv.sh
%config(noreplace) %{bamboodatadir}/atlassian-%{name}/WEB-INF/classes/%{name}-init.properties
%{_unitdir}/%{name}.service

%changelog
* Wed Dec 12 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.7.2-1
- Update to 6.7.2
* Fri Oct 19 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.7.1-1
- Update to 6.7.1
* Thu Sep 27 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.6.3-1
- Update to 6.6.3
* Fri Aug 17 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.6.2-1
- Update to 6.6.2
* Fri Jul 06 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.6.1-1
- Update to 6.6.1
* Wed Jun 27 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.6.0-1
- Update to 6.6.0
* Sat Jun 23 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.5.1-1
- Update to 6.5.1
* Wed Apr 25 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.5.0-1
- Update to 6.5.0
* Thu Mar 22 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.4.1-1
- Update to 6.4.1
* Thu Feb 22 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.4.0-1
- Update to 6.4.0
* Tue Feb 06 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.3.2-1
- Update to 6.3.2
* Tue Jan 16 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.3.1-1
- Update to 6.3.1
* Thu Jan 04 2018 Martin Hagstrom (API) <marhag87@gmail.com> 6.3.0-1
- Update to 6.3.0
* Mon Dec 18 2017 Martin Hagstrom <marhag87@gmail.com> 6.2.5-2
- Systemd service file should not be executable
* Tue Dec 12 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.2.5-1
- Update to 6.2.5
* Wed Nov 22 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.2.3-1
- Update to 6.2.3
* Tue Oct 17 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.2.2-1
- Update to 6.2.2
* Fri Sep 29 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.2.1-1
- Update to 6.2.1
* Sat Aug 12 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.1.1-1
- Update to 6.1.1
* Fri Jul 21 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.1.0-1
- Update to 6.1.0
* Thu Jun 08 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.0.3-1
- Update to 6.0.3
* Tue Jun 06 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.0.2-1
- Update to 6.0.2
* Tue May 23 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.0.1-1
- Update to 6.0.1
* Wed Apr 26 2017 Martin Hagstrom (API) <marhag87@gmail.com> 6.0.0-1
- Update to 6.0.0
* Tue Mar 28 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.15.5-1
- Update to 5.15.5
* Fri Mar 24 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.15.4-1
- Update to 5.15.4
* Thu Mar 09 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.15.3-1
- Update to 5.15.3
* Wed Mar 08 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.15.2-1
- Update to 5.15.2
* Tue Feb 21 2017 Martin Hagstrom <marhag87@gmail.com> 5.15.0.1-2
- Require java on Fedora
* Tue Feb 14 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.15.0.1-1
- Update to 5.15.0.1
* Tue Jan 24 2017 Martin Hagstrom <marhag87@gmail.com> 5.14.4.1-2
- Update mysql connector to 5.1.40
* Thu Jan 12 2017 Martin Hagstrom (API) <marhag87@gmail.com> 5.14.4.1-1
- Update to 5.14.4.1
* Mon Dec 05 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.14.3.1-1
- Update to 5.14.3.1
* Fri Nov 04 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.14.1-1
- Update to 5.14.1
* Mon Oct 31 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.14.0.2-1
- Update to 5.14.0.2
* Thu Oct 27 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.14.0.1-1
- Update to 5.14.0.1
* Thu Sep 29 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.13.2-1
- Update to 5.13.2
* Wed Sep 21 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.13.1-1
- Update to 5.13.1
* Thu Aug 25 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.13.0.1-1
- Update to 5.13.0.1
* Tue Jul 12 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.12.3.1-1
- Update to 5.12.3.1
* Thu Jun 16 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.12.2.1-1
- Update to 5.12.2.1
* Wed Jun 01 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.12.2-1
- Update to 5.12.2
* Thu May 26 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.12.1-1
- Update to 5.12.1
* Tue May 24 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.12.0.2-1
- Update to 5.12.0.2
* Fri May 13 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.11.3-1
- Update to 5.11.3
* Thu Apr 28 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.11.1.1-1
- Update to 5.11.1.1
* Tue Apr 26 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.11.1-1
- Update to 5.11.1
* Wed Mar 16 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.10.3-1
- Update to 5.10.3
* Wed Mar 02 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.10.2-1
- Update to 5.10.2
* Tue Feb 09 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.10.1.1-1
- Update to 5.10.1.1
* Tue Jan 19 2016 Martin Hagstrom <marhag87@gmail.com> 5.10.0-2
- Update server.xml file for 5.10.0
- Use systemd service file
* Tue Jan 19 2016 Martin Hagstrom (API) <marhag87@gmail.com> 5.10.0-1
- Update to 5.10.0
* Sat Dec 19 2015 Martin Hagstrom <marhag87@gmail.com> 5.9.7-3
- Don't get osgi provides and requires
* Sat Dec 19 2015 Martin Hagstrom <marhag87@gmail.com> 5.9.7-2
- Don't build debug package
* Fri Dec 11 2015 Martin Hagstrom <marhag87@gmail.com> 5.9.7-1
- Initial release
