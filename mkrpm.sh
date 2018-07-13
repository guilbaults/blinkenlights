#!/bin/bash
spectool -g -R blinkenlights-el7.spec
rpmbuild --define "dist .el7" -ba blinkenlights-el7.spec
