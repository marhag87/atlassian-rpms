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
Source5:            bamboo.te
Source6:            bamboo.fc
Source7:            bamboo.if
Source8:            bitbucket.te
Source9:            bitbucket.fc
Source10:           bitbucket.if
Source11:           jira.te
Source12:           jira.fc
Source13:           jira.if

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
   %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} \
   %{SOURCE8} %{SOURCE9} %{SOURCE10} %{SOURCE11} \
   %{SOURCE12} %{SOURCE13} \
.

%build
for i in atlassian confluence bamboo bitbucket jira
do
  make -f /usr/share/selinux/devel/Makefile ${i}.pp || exit
done

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 0644 *.pp %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 0644 *.if %{buildroot}%{_datadir}/selinux/devel/include/contrib/

%post
for i in atlassian confluence bamboo bitbucket jira
do
    semodule -n -i %{_datadir}/selinux/packages/${i}.pp
done

if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    for i in confluence bamboo bitbucket jira
    do
        fixfiles -R ${i} restore
    done
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
    for i in confluence bamboo bitbucket jira atlassian
    do
        semodule -n -r ${i}
    done

    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
    fi;
fi;
exit 0

%files
%defattr(-,root,root,-)
%{_datadir}/selinux/packages/*.pp
%{_datadir}/selinux/devel/include/contrib/*.if

%changelog
* Wed Jan 17 2018 Robert FÜhricht <robert.fuehricht@jku.at> - 1.0-1
- Initial version

