from fabric import Connection
from invoke import run, task


def main():
    run('git push')
    c = Connection('powerkit@104.248.132.201')
    c.run('source /home/powerkit/envs/kit/bin/activate; cd /home/powerkit/webapps/powertoolkit/powerkit/; git pull; ./manage.py migrate; ./manage.py collectstatic --noinput; supervisorctl restart powerkit;')
    c.run('pwd')

if __name__ == '__main__':
    main()
