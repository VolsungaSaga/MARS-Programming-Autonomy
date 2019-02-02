#!/bin/sh
git pull --recurse-submodules
git submodule foreach "git pull origin master && git checkout master"