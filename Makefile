TOPDIR=$(shell git rev-parse --show-toplevel)

all: jira confluence bitbucket bamboo

jira: clean
	rpmbuild --define "_topdir $(TOPDIR)" -bb SPECS/jira.spec
	mv RPMS/x86_64/jira-*.rpm .

confluence: clean
	rpmbuild --define "_topdir $(TOPDIR)" -bb SPECS/confluence.spec
	mv RPMS/x86_64/confluence-*.rpm .

bitbucket: clean
	rpmbuild --define "_topdir $(TOPDIR)" -bb SPECS/bitbucket.spec
	mv RPMS/x86_64/bitbucket-*.rpm .

bamboo: clean
	rpmbuild --define "_topdir $(TOPDIR)" -bb SPECS/bamboo.spec
	mv RPMS/x86_64/bamboo-*.rpm .

clean:
	rm -rf BUILD BUILDROOT RPMS SRPMS || true
