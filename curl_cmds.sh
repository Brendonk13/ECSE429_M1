# bash curl_cmds.sh all will return all todo's

# to test error:
# $ bash curl_cmds.sh post

do_test() {
    if [ $# -lt 1 ]; then
        echo 'USAGE: bash curl_cmds.sh [post |get |del |all] [endpoint <- default = todos]'
        exit 1
    fi
    ID=1
    endpoint=''

    if [ $# -eq 2 ]; then
        endpoint="$2"
        echo "endpoint: [ $endpoint ], method = [ $1 ], ID: [ $ID ]"
        # return
    else
        endpoint='todos'
    fi

    if [ "$1" = "post" ]; then
        echo '--POST'
        curl -X POST -d '{"title":"new todo"}' -H 'Content-Type: application/json'  http://localhost:4567/$endpoint/
        echo '--now POST WITHOUT trailing slash'
        curl -X POST -d '{"title":"new todo"}' -H 'Content-Type: application/json'  http://localhost:4567/$endpoint

    elif [ "$1" = "get" ]; then
        echo 'GET'
        curl -X GET -H 'Content-Type: application/json'  http://localhost:4567/$endpoint/$ID

    elif [ "$1" = 'del' ]; then
        echo 'DELETE'
        curl -X DELETE -H 'Content-Type: application/json'  http://localhost:4567/$endpoint/$ID
        echo  '   VERIFY DELETED, NEW ALL:'
        curl -X GET -H 'Content-Type: application/json'  http://localhost:4567/$endpoint

    elif [ "$1" = 'all' ]; then
        # get all todo's
        echo 'ALL'
        curl -X GET -H 'Content-Type: application/json'  http://localhost:4567/$endpoint
    fi
    echo ''
    echo '------------------------------------------------------------------------'
}

# declare -a endpoints=('projects/1/tasks' 'projects/1/categories' 'todos/1/tasksof' 'todos/1/categories' 'todos' 'projects' 'categories')
declare -a endpoints=('categories' 'categories/2/todos' 'categories/2/projects')
declare -a req_types=('get')

if [ $# -eq 0 ]; then
    # do_test all
    for endpoint in "${endpoints[@]}"; do
        do_test all "$endpoint"
        for req_type in "${req_types[@]}"; do
            do_test "$req_type" "$endpoint"
        done
    done
else
    do_test "$1"
fi
