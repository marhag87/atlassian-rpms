# vim: sw=4:ts=4:et
Name:               atlassian-selinux
Version:            1.0
Release:            1%{?dist}
Summary:            SELinux policy module for various beats
BuildArch:          noarch

Group:              System Environment/Base     
License:            GPLv2+  
URL:                https://git.im.jku.at/summary/packages!beats-selinux.git
Source0:            atlassian.te
Source1:            atlassian.if
Source2:            confluence.te
Source3:            confluence.fc
Source4:            confluence.if

BuildRequires:      selinux-policy-devel >= 3.13
BuildRequires:      policycoreutils-devel
Requires:           policycoreutils
Requires:           libselinux-utils
Requires(post):     policycoreutils, policycoreutils-python 
Requires(postun):   policycoreutils, policycoreutils-python 

%description
This package installs and sets up the SELinux policy security module for Atlassian
products..

%prep
%setup -c -n %{name} -T
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} \
   %{SOURCE4} \
 .

%build
make -f /usr/share/selinux/devel/Makefile atlassian.pp || exit
make -f /usr/share/selinux/devel/Makefile confluence.pp || exit

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 0644 atlassian.pp %{buildroot}%{_datadir}/selinux/packages
install -m 0644 confluence.pp %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 0644 atlassian.if %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -m 0644 confluence.if %{buildroot}%{_datadir}/selinux/devel/include/contrib/

%post
semodule -n -i %{_datadir}/selinux/packages/atlassian.pp
semodule -n -i %{_datadir}/selinux/packages/confluence.pp

if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    fixfiles -R atlassian
    fixfiles -R confluence
fi;

#semanage port -p tcp -t logstash_port_t -a 5044
#semanage port -p tcp -t kafka_port_t -a 9092
#semanage port -p tcp -t elasticsearch_port_t -a 9200
exit 0
 
%postun
if [ $1 -eq 0 ]; then
#    semanage port -p tcp -t logstash_port_t -d 5044
#    semanage port -p tcp -t kafka_port_t -d 9092
#    semanage port -p tcp -t elasticsearch_port_t -d 9200

    semodule -n -r confluence
    semodule -n -r atlassian

    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
    fi;
fi;
exit 0

%files
%defattr(-,root,root,-)
%{_datadir}/selinux/packages/atlassian.pp
%{_datadir}/selinux/packages/confluence.pp
%{_datadir}/selinux/devel/include/contrib/atlassian.if
%{_datadir}/selinux/devel/include/contrib/confluence.if

%changelog
* Wed Jan 17 2018 Robert FÜhricht <robert.fuehricht@jku.at> - 1.0-1
- Initial version

