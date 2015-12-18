TOPDIR=$(shell git rev-parse --show-toplevel)

all: jira confluence bitbucket bamboo

define version =
$(shell awk '/^Version/ {print $$2}' SPECS/$@.spec)
endef

define build =
rpmbuild --define "_topdir $(TOPDIR)" -bb SPECS/$@.spec
mv RPMS/x86_64/$@-*.rpm .
endef

jira: clean
	test -s SOURCES/atlassian-jira-software-$(version)-jira-$(version).tar.gz || wget https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-software-$(version)-jira-$(version).tar.gz -O SOURCES/atlassian-jira-software-$(version)-jira-$(version).tar.gz
	$(build)

confluence: clean
	test -s SOURCES/atlassian-confluence-$(version).tar.gz || wget https://www.atlassian.com/software/confluence/downloads/binary/atlassian-confluence-$(version).tar.gz -O SOURCES/atlassian-confluence-$(version).tar.gz
	$(build)

bitbucket: clean
	test -s SOURCES/atlassian-bitbucket-$(version).tar.gz || wget https://www.atlassian.com/software/stash/downloads/binary/atlassian-bitbucket-$(version).tar.gz -O SOURCES/atlassian-bitbucket-$(version).tar.gz
	$(build)

bamboo: clean
	test -s SOURCES/atlassian-bamboo-$(version).tar.gz || wget https://www.atlassian.com/software/bamboo/downloads/binary/atlassian-bamboo-$(version).tar.gz -O SOURCES/atlassian-bamboo-$(version).tar.gz
	$(build)

clean:
	rm -rf BUILD BUILDROOT RPMS SRPMS || true
