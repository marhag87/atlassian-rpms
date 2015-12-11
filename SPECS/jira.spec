Name:           jira
Version:        7.0.4
Release:        1%{?dist}
Summary:        An issue tracking web application

License:        Proprietary
URL:            https://www.atlassian.com/software/jira
Source0:        atlassian-%{name}-software-%{version}-%{name}-%{version}.tar.gz
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

%define jiradatadir %{_datarootdir}/atlassian/%{name}
%define jirahomedir %{_localstatedir}/atlassian/application-data/%{name}
%define jiralogdir  %{_localstatedir}/log/atlassian/%{name}

%description
An issue tracking web application

%prep
%setup -q -n "atlassian-%{name}-software-%{version}-standalone"

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
  /etc/init.d/%{name} stop > /dev/null 2>&1
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
* Fri Dec 11 2015 Martin Hagstrom <marhag87@gmail.com> 7.0.4-1
- Initial release
