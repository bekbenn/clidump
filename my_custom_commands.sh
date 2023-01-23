#!/bin/bash
function log_in() {
    python3 -c 'import dump; dump.log_in()'
}
function log_out() {
    python3 -c 'import dump; dump.log_out()'
}
function bd() {
    python3 -c 'import sys, dump; dump.bd(sys.argv[1])' "$*"
}
function sbt() {
    python3 -c 'import sys, dump; dump.sbt(sys.argv[1])' "$*"
}
function vd() {
    python3 -c 'import dump; dump.vd()'
}
function rd() {
    python3 -c 'import dump; dump.rd()'
}
function ed() {
    python3 -c 'import dump; dump.ed()'
}

