# An Itty-Bitty `wsloader` Example

Here's an example based on what I wrote on-the-fly with my laptop
projected on screen for a tech-talk about wsloader. It's not that I
don't have stage-fright, it's just that wsloader is incredibly
easy. So let's dip our toes in, shall we?

## 1. Getting Started

Before getting started with this example, you should have wsloader
installed correctly. For this example we'll use a Python module,
greeter.py, from the 'tests' directory in wsloader source
distribution. It should be copied to a standard directory where you
would install python modules. For RHEL, this is the "site-packages"
directory for Python in your system. The following command could help
you find it:

``locate site-packages | grep `python -V 2>&1 | awk '{print $2}' | cut -d . -f -2` ``

For Ubuntu, this directory is `dist-packages`.

## 2. Hello World

Let's say we have the following module
```python
// greeter.py
def say_hello():
    return "Hello World!"

def service_check():
    return {"status": 200, "body": "OK"}

class Greeter:
    def __init__(self, greeting):
        self.greeting = greeting
    def say_hello(self, to_whom = "World!"):
        return "%s %s" % (self.greeting, to_whom)
```

The simplest of these services is the hello_world function in
greeter. To expose this in wsloader, you only have to create a file
called `examples.ini` in `/etc/wsloader-wsgi/`. The file name actually
doesn't matter. In its contents, just mention the name of the module
to be loaded, in square brackets. It should look something like this:
```sh
$ cat /etc/wsloader-wsgi/examples.ini
[greeter]

$
```

That's it. You just need the module name to be listed in the ini file. When you restart httpd after creating this config file, you can use the URL `http://localhost/services/greeter/say_hello` for the following Python equivalent:
```python
>>> import greeter
>>> greeter.say_hello()
'Hello World!'
>>> 
```

## 2. Advanced Configuration

`greeter.py` module contains a class, `Greeter`. By default, it would be referred by wsloader as `localhost/services/greeter.Greeter`. The class takes an
``__init__`` parameter, `greeting` and its `say_hello()` method takes an argument, `to_whom`.

Normally, to expose this class, you'd add a line that reads
"[greeter.Greeter]" in the config file. The resulting service URL
would be:

```http://localhost/services/greeter/Greeter/```

How about making it slightly more pretty? We shall change
`greeter.Greeter` to "helloworld". To do that, replace ``[greeter.Greeter]`` in the `ini` config file
with ``[helloworld]`` instead, and under it, add the following directive:

    alias_to=greeter.Greeter 

So the config file now looks like this:
```sh
$ cat /etc/wsloader-wsgi/examples.ini
[greeter]

[helloworld]
alias_to=greeter.Greeter

$
```

Since Greeter is a class that takes "greeting" as an
``__init__`` parameter, we also need to specify the following:

    type=class
    init_param=greeting

With these three directives placed, the configuration finally looks like this:
```sh
$ cat /etc/wsloader-wsgi/examples.ini
[greeter]

[helloworld]
alias_to=greeter.Greeter
type=class
init_param=greeting

$
```

To call the web-service equivalent of the following invocation:
```python
>>> from greeter import Greeter
>>> Greeter("Hello").say_hello("World")
'Hello World'
>>> 
```
you can use the following URL:
```
http://localhost/services/helloworld/say_hello?greeting="Hello"&to_whom="World"
```

That's it! That's our Hello World example. The complete config file is provided in tests/conf/examples.ini.

