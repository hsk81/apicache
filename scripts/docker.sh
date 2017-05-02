#!/bin/bash
###############################################################################
SCRIPT_PATH=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd) ;
###############################################################################

source ${SCRIPT_PATH}/conf/build.sh

###############################################################################
###############################################################################

if [ -x "$(command -v docker.io)" ];
    then DOCKER_CMD=docker.io ;
fi;

if [ -x "$(command -v docker)" ];
    then DOCKER_CMD=docker ;
fi;

###############################################################################
###############################################################################

function git_archive () {
    rm -f ${1}.zip && git archive -o ${1}.zip ${1}
}

function git_archive_rm () {
    rm -f ${1}.zip
}

###############################################################################
###############################################################################

function docker_build () {
    $DOCKER_CMD build -t ${1} .
}

function docker_run () {
    $DOCKER_CMD run --name ${1} -d -p ${2} ${3} ${@:5}
}

function docker_dev () {
    $DOCKER_CMD run --name ${1} -t -p ${2} ${3} ${@:5}
}

function docker_rm () {
    $DOCKER_CMD kill ${1} 2> /dev/null ;
    $DOCKER_CMD rm ${1} 2> /dev/null ;
}

###############################################################################
###############################################################################

case ${1} in

    all)
        git_archive ${GIT_REFNAME} && docker_build ${DEF_IMGNAME} && \
        docker_rm ${DEF_APPNAME} && git_archive_rm ${GIT_REFNAME}
        docker_run ${DEF_APPNAME} ${DEF_PORTMAP} ${DEF_IMGNAME} $@ ;;
    build)
        git_archive ${GIT_REFNAME} && \
        docker_build ${DEF_IMGNAME} ;;
    rm)
        docker_rm ${DEF_APPNAME} ;;
    run)
        docker_run ${DEF_APPNAME} ${DEF_PORTMAP} ${DEF_IMGNAME} $@ ;;
    dev)
        docker_dev ${DEF_APPNAME} ${DEF_PORTMAP} ${DEF_IMGNAME} $@ ;;
    *)
        $0 all $@ ;;
esac

###############################################################################
###############################################################################

exit 0
