%define base_name wsloader-wsgi
%define wsgi_dir /var/www/wsgi

%define httpd_config_dir /etc/httpd/conf.d
%define wdp_config_dir /etc/wsloader-wsgi

Summary: Webservice Delivery Platform
Name: %{base_name}
Version: 1.0
Release: 1
License: None
Group: Applications/Internet
Source: %{name}-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-root
Requires: mod_wsgi >= 2.5, mod_wsgi < 3
Requires: python-werkzeug >= 0.5-1, python-werkzeug < 1
BuildRequires: python25
BuildArch: noarch

%description
A WSGI Application that allows exposing regular Python modules or
public class methods as JSON-HTTP webservices using apache2 and
mod_wsgi

%prep
%setup -q

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{wsgi_dir}
install -d $RPM_BUILD_ROOT%{httpd_config_dir}
install -d $RPM_BUILD_ROOT%{wdp_config_dir}
install -m 644 wsloader.py $RPM_BUILD_ROOT%{wsgi_dir}/wsloader.py
install -m 644 wsloader.conf $RPM_BUILD_ROOT%{httpd_config_dir}/wsloader.conf

%post
if [[ `/sbin/service httpd status` != "httpd is stopped" ]];
    then /sbin/service httpd restart;
fi

%postun
if [[ `/sbin/service httpd status` != "httpd is stopped" ]];
    then /sbin/service httpd restart;
fi

%files
%{wsgi_dir}/wsloader.py
%{httpd_config_dir}/wsloader.conf

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
