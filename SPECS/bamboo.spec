Name:           bamboo
Version:        5.9.7
Release:        2%{?dist}
Summary:        A continuous integration web application

License:        Proprietary
URL:            https://www.atlassian.com/software/bamboo
Source0:        https://www.atlassian.com/software/bamboo/downloads/binary/atlassian-%{name}-%{version}.tar.gz
Source1:        %{name}.init
Source2:        %{name}-server.xml
Source3:        mysql-connector-java-5.1.37-bin.jar
Source4:        %{name}-init.properties
Source5:        stop-%{name}.sh
Source6:        %{name}-setenv.sh
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root

AutoReqProv:    no
Requires:       java-1.8.0-oracle
Requires(pre):  shadow-utils

# Don't repackage jar files
%define __jar_repack %{nil}

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
install -p -d -m 0755 %{buildroot}%{_sysconfdir}/init.d

mv * %{buildroot}%{bamboodatadir}/

install -p -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/%{name}
install -p -m 0644 %{SOURCE2} %{buildroot}%{bamboodatadir}/conf/server.xml
install -p -m 0644 %{SOURCE3} %{buildroot}%{bamboodatadir}/lib/mysql-connector-java-5.1.37-bin.jar
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
%{_sysconfdir}/init.d/%{name}

%changelog
* Sat Dec 19 2015 Martin Hagstrom <marhag87@gmail.com> 5.9.7-2
- Don't build debug package
* Fri Dec 11 2015 Martin Hagstrom <marhag87@gmail.com> 5.9.7-1
- Initial release
