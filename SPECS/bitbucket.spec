Name:           bitbucket
Version:        4.5.2
Release:        1%{?dist}
Summary:        A GIT repository web application

License:        Proprietary
URL:            https://www.atlassian.com/software/bitbucket
Source0:        https://www.atlassian.com/software/stash/downloads/binary/atlassian-%{name}-%{version}.tar.gz
Source1:        %{name}.init
Source2:        %{name}-server.xml
Source3:        mysql-connector-java-5.1.37-bin.jar
Source4:        %{name}-user.sh
Source5:        %{name}-setenv.sh
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires:       java-1.8.0-oracle
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
install -p -d -m 0755 %{buildroot}%{_sysconfdir}/init.d

mv * %{buildroot}%{bitbucketdatadir}/

install -p -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/%{name}
install -p -m 0644 %{SOURCE2} %{buildroot}%{bitbucketdatadir}/conf/server.xml
install -p -m 0644 %{SOURCE3} %{buildroot}%{bitbucketdatadir}/lib/mysql-connector-java-5.1.37-bin.jar
install -p -m 0644 %{SOURCE4} %{buildroot}%{bitbucketdatadir}/bin/user.sh
install -p -m 0755 %{SOURCE5} %{buildroot}%{bitbucketdatadir}/bin/setenv.sh

rmdir %{buildroot}%{bitbucketdatadir}/logs
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
