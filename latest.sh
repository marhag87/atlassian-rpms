#!/bin/bash
# Script for checking for new versions of atlassian products
# Written by Martin Hagström 2015-12-17

function getlatestversion() {
  curl -s https://my.atlassian.com/download/feeds/current/${1}.json | sed 's/.*"\(.*-\([[:digit:].]*\)\.tar\.gz\)".*/\2/'
}

function getcurrentversion() {
  awk '/^Version/ { print $2 }' SPECS/${1}.spec
}

function compareversions() {
  latestversion=$(getlatestversion ${2:-$1})
  currentversion=$(getcurrentversion $1)
  if [[ $currentversion != $latestversion ]]; then
    echo "$1 not up to date, latest version: ${latestversion}"
  fi
}

if [[ -z $1 ]]; then
  compareversions jira jira-software
  compareversions bitbucket stash
  compareversions confluence
  compareversions bamboo
else
  compareversions $@
fi
