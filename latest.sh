#!/bin/bash
# Script for checking for new versions of atlassian products
# Written by Martin Hagström 2015-12-17

update=false

function getlatestversion() {
  curl -s https://my.atlassian.com/download/feeds/current/${1}.json | sed 's/.*"\(.*-\([[:digit:].]*\)\.tar\.gz\)".*/\2/'
}

function getcurrentversion() {
  awk '/^Version/ { print $2 }' SPECS/${1}.spec
}

function update() {
  datestring=$(date "+%a %b %d %Y Martin Hagstrom (API) <marhag87@gmail.com> $2-1")
  sed -i "s/\(^Version:\s*\)[[:digit:].]*/\1${2}/"   SPECS/${1}.spec
  sed -i "s/\(^Release:\s*\)[[:digit:].]*/\11/"      SPECS/${1}.spec
  sed -i "s/\%changelog/\%changelog\n\* ${datestring}\n- Update to $2/" SPECS/${1}.spec
}

function compareversions() {
  latestversion=$(getlatestversion ${2:-$1})
  currentversion=$(getcurrentversion $1)
  if [[ $currentversion != $latestversion ]]; then
    if [[ $update == true ]]; then
      update $1 $latestversion
    else
      echo "$1 not up to date, latest version: ${latestversion}"
    fi
  fi
}

while getopts ":u" opt; do
  case $opt in
    u)
      update=true
      shift
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

if [[ -z $1 ]]; then
  compareversions jira jira-software
  compareversions bitbucket stash
  compareversions confluence
  compareversions bamboo
else
  compareversions $@
fi
