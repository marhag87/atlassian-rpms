TOPDIR=$(shell git rev-parse --show-toplevel)
JIRAVERSION=$(shell awk '/^Version/ {print $$2}' SPECS/jira.spec)
CONFLUENCEVERSION=$(shell awk '/^Version/ {print $$2}' SPECS/confluence.spec)
BITBUCKETVERSION=$(shell awk '/^Version/ {print $$2}' SPECS/bitbucket.spec)
BAMBOOVERSION=$(shell awk '/^Version/ {print $$2}' SPECS/bamboo.spec)

all: jira confluence bitbucket bamboo

jira: clean
	test -s SOURCES/atlassian-jira-software-$(JIRAVERSION)-jira-$(JIRAVERSION).tar.gz || wget https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-software-$(JIRAVERSION)-jira-$(JIRAVERSION).tar.gz -O SOURCES/atlassian-jira-software-$(JIRAVERSION)-jira-$(JIRAVERSION).tar.gz
	rpmbuild --define "_topdir $(TOPDIR)" -bb SPECS/jira.spec
	mv RPMS/x86_64/jira-*.rpm .

confluence: clean
	test -s SOURCES/atlassian-confluence-$(CONFLUENCEVERSION).tar.gz || wget https://www.atlassian.com/software/confluence/downloads/binary/atlassian-confluence-$(CONFLUENCEVERSION).tar.gz -O SOURCES/atlassian-confluence-$(CONFLUENCEVERSION).tar.gz
	rpmbuild --define "_topdir $(TOPDIR)" -bb SPECS/confluence.spec
	mv RPMS/x86_64/confluence-*.rpm .

bitbucket: clean
	test -s SOURCES/atlassian-bitbucket-$(BITBUCKETVERSION).tar.gz || wget https://www.atlassian.com/software/stash/downloads/binary/atlassian-bitbucket-$(BITBUCKETVERSION).tar.gz -O SOURCES/atlassian-bitbucket-$(BITBUCKETVERSION).tar.gz
	rpmbuild --define "_topdir $(TOPDIR)" -bb SPECS/bitbucket.spec
	mv RPMS/x86_64/bitbucket-*.rpm .

bamboo: clean
	test -s SOURCES/atlassian-bamboo-$(BAMBOOVERSION).tar.gz || wget https://www.atlassian.com/software/bamboo/downloads/binary/atlassian-bamboo-$(BAMBOOVERSION).tar.gz -O SOURCES/atlassian-bamboo-$(BAMBOOVERSION).tar.gz
	rpmbuild --define "_topdir $(TOPDIR)" -bb SPECS/bamboo.spec
	mv RPMS/x86_64/bamboo-*.rpm .

clean:
	rm -rf BUILD BUILDROOT RPMS SRPMS || true
