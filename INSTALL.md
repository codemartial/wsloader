# Installing `wsloader`

## 1. Install `werkzeug` and `libapache2-mod-wsgi`

This guide assumes that you have a working installation of `apache2` webserver. It uses `libapache2-mod-wsgi` module to enable python execution from `apache2` using the Python `WSGI` protocol. `werkzeug` is the Python middleware for handling WSGI requests.

   * `sudo apt-get install werkzeug libapache2-mod-wsgi` on Ubuntu
   * `sudo yum install werkzeug mod_wsgi` on Fedora
   * Try `sudo easy_install werkzeug` if it's not available in your OS's repository

## 2. Install `wsloader`

Install `src/wsloader.py` in `/var/www/wsgi/` directory

```sh
$ git clone git@github.com:codemartial/wsloader.git
Cloning into 'wsloader'...

$ sudo install -d /var/www/wsgi
$ sudo install -m 644 src/wsloader.py /var/www/wsgi
```


## 3. Set up `wsloader`

Install `config/wsloader.conf` in apache's `conf.d` directory,
wherever it lives on your system 

``$ sudo install -m 644 config/wsloader.conf /etc/httpd/conf.d/`` on Red Hat based distributions

``sudo install -m 644 config/wsloader.conf /etc/apache2/conf.d`` on Ubuntu

## 4. Restart httpd. 

Please note that the default config in wsloader.conf re-routes all URLs starting with /services to wsloader. If you want to restrict this to a different sub-path -- `examplepath` -- substitute:

`WSGIScriptAlias /services /var/www/wsgi/wsloader.py`

with

`WSGIScriptAlias /examplepath /var/www/wsgi/wsloader.py`

inside `wsloader.conf` file.

## 5. Try it out

Look at the [Quick Start Guide](example.md) for a demo service to test the installation.