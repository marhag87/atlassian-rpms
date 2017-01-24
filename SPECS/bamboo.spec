Name:           bamboo
Version:        5.14.4.1
Release:        2%{?dist}
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
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root

AutoReqProv:    no
Requires:       java-1.8.0-oracle
Requires(pre):  shadow-utils
BuildRequires:  systemd

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

%description
A continuous integration web application

%prep
%setup -q -n "atlassian-%{name}-%{version}"

%build

%install
install -p -d -m 0755 %{buildroot}%{bamboodatadir}
install -p -d -m 0755 %{buildroot}%{bamboohomedir}
install -p -d -m 0755 %{buildroot}%{bamboologdir}
install -p -d -m 0755 %{buildroot}%{_unitdir}

mv * %{buildroot}%{bamboodatadir}/

install -p -m 0755 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -m 0644 %{SOURCE2} %{buildroot}%{bamboodatadir}/conf/server.xml
install -p -m 0644 %{SOURCE3} %{buildroot}%{bamboodatadir}/lib/mysql-connector-java-%{mysqlconnectorversion}-bin.jar
install -p -m 0644 %{SOURCE4} %{buildroot}%{bamboodatadir}/atlassian-%{name}/WEB-INF/classes/%{name}-init.properties
install -p -m 0755 %{SOURCE5} %{buildroot}%{bamboodatadir}/bin/stop-%{name}.sh
install -p -m 0755 %{SOURCE6} %{buildroot}%{bamboodatadir}/bin/setenv.sh

rmdir %{buildroot}%{bamboodatadir}/logs
ln -sf %{bamboologdir} %{buildroot}%{bamboodatadir}/logs

%clean
rm -rf %{buildroot}

%pre
/etc/init.d/%{name} stop > /dev/null 2>&1
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{bamboohomedir} -s /bin/bash \
    -c "Bamboo user" %{name}
exit 0

%preun
if [ $1 -eq 0 ] ; then
  /etc/init.d/%{name} stop > /dev/null 2>&1
fi

%files
%defattr(-,bamboo,bamboo)
%{bamboodatadir}
%{bamboohomedir}
%{bamboologdir}
%config(noreplace) %{bamboodatadir}/conf/server.xml
%config(noreplace) %{bamboodatadir}/bin/setenv.sh
%config(noreplace) %{bamboodatadir}/atlassian-%{name}/WEB-INF/classes/%{name}-init.properties
%{_unitdir}/%{name}.service

%changelog
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
