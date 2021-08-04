echo ${PWD}
echo "开始停止服务"
ps -ef | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill -9

echo "开始启动服务"
${PWD}/venv/bin/gunicorn -c ${PWD}/gconfig.py cyclone:app -k uvicorn.workers.UvicornWorker --reload &
