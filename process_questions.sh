#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR/face
python manage.py qpurge
python manage.py parseall
python manage.py solveall
