#!/bin/bash

function version() {
  awk '/^Version/ {print $2}' SPECS/$1.spec
}

function build() {
  rm -rf BUILD BUILDROOT RPMS SRPMS || true
  test -s SOURCES/atlassian-$1-$(version $1).tar.gz
  if [[ $? -ne 0 ]]; then
    wget https://downloads.atlassian.com/software/${2:-$1}/downloads/atlassian-${3:-$1}-$(version $1).tar.gz -O SOURCES/atlassian-$1-$(version $1).tar.gz
    gunzip SOURCES/atlassian-$1-$(version $1).tar.gz
    mv SOURCES/atlassian-$1-$(version $1).tar SOURCES/atlassian-$1-$(version $1).tar.gz
  fi
  rpmbuild --define "_topdir $(git rev-parse --show-toplevel)" -bb SPECS/$1.spec
  mv RPMS/x86_64/$1-*.rpm .
}

if [[ -z $1 ]]; then
  $0 bamboo
  $0 bitbucket
  $0 confluence
  $0 jira
else
  case $1 in
    jira)
      build jira jira jira-software
      ;;
    bitbucket)
      build bitbucket stash
      ;;
    *)
      build $1
      ;;
  esac
fi
