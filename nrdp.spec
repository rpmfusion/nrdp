# TODO: unbundle JS from server/includes
# - jquery 3.2.1
# - bootstrap 4.0.0-beta2

Name:    nrdp
Version: 1.5.2
Release: 3%{?dist}
Summary: Nagios Remote Data Processor

# NRDP php client is BSD
# Bundled jquery and boostrap are MIT
# Everything else is Nagios Open Software License (which is non-free)
License: Nagios Open Software License and BSD and MIT
URL:     https://github.com/NagiosEnterprises/nrdp
Source0: https://github.com/NagiosEnterprises/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Source1: %{name}-httpd.conf
Source2: %{name}-config.inc.php

BuildArch: noarch

Requires: nagios
# For clarity since Nagios should pull them
Requires: httpd
Requires: mod_php

Provides: bundled(js-jquery) = 3.2.1
Provides: bundled(js-bootstrap) = 4.0.0


%description
Nagios Remote Data Processor (NDRP) is a flexible data transport
mechanism and processor for Nagios. It is designed with a simple
and powerful architecture that allows for it to be easily extended
and customized to fit individual users needs. It uses standard ports
protocols (HTTP(S) and XML) and can be implemented as a replacement for NSCA.


%package client-shell
Summary: Send NRDP shell script for Nagios
%description client-shell
A shell script to send NRDP data to a Nagios server.

%package client-php
Summary: Send NRDP php script for Nagios
License: BSD
%description client-php
A php script to send NRDP data to a Nagios server.

%package client-python
Summary: Send NRDP python script for Nagios
%description client-python
A python script to send NRDP data to a Nagios server.


%prep
%setup -q
# Fix perms
chmod a-x server/includes/bootstrap.bundle.min.js
chmod a-x server/includes/bootstrap.min.css
chmod a-x server/includes/jquery-3.2.1.min.js
# Fix shebang
sed -i -e '1d;2i#!/usr/bin/python2' clients/send_nrdp.py
# Fix EOL
sed -i "s|\r||g" clients/send_nrdp.php


%build
# Nothing here


%install
# Server
mkdir -p %{buildroot}%{_datadir}/%{name}/
rm -f  server/config.inc.php
cp -pr server/*  %{buildroot}%{_datadir}/%{name}/
ln -s %{_sysconfdir}/%{name}/config.inc.php \
    ${RPM_BUILD_ROOT}%{_datadir}/%{name}/config.inc.php
# Server conf file
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/
install -m 0644 -D -p %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/config.inc.php
# httpd conf
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -m 0644 -D -p %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/nrdp.conf
# Client scripts
mkdir -p %{buildroot}%{_bindir}/
install -m 0755 -D -p clients/* %{buildroot}%{_bindir}/


%files
%license LICENSE.md
%doc CHANGES.md README.md
%{_datadir}/%{name}/
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/config.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/nrdp.conf

%files client-shell
%license LICENSE.md
%{_bindir}/send_nrdp.sh

%files client-php
%license LICENSE.md
%{_bindir}/send_nrdp.php

%files client-python
%license LICENSE.md
%{_bindir}/send_nrdp.py


%changelog
* Tue Mar 05 2019 Xavier Bachelot <xavier@bachelot.org> 1.5.2-3
- Mark python client as python2.

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 12 2018 Xavier Bachelot <xavier@bachelot.org> 1.5.2-1
- Update to 1.5.2.
- Fix License: tag for php client sub-package.

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.1-6
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 26 2018 Xavier Bachelot <xavier@bachelot.org> 1.5.1-4
- Clarify license.
- Own %%{_sysconfdir}/%%{name}.
- Requires mod_php rather than php.

* Fri Feb 23 2018 Athmane Madjoudj <athmane@fedoraproject.org> - 1.5.1-3
- Revamp requirements

* Fri Feb 23 2018 Xavier Bachelot <xavier@bachelot.org> 1.5.1-2
- More clean up.

* Fri Feb 23 2018 Xavier Bachelot <xavier@bachelot.org> 1.5.1-1
- Update to 1.5.1.
- Clean up spec.

* Sat Nov 21 2015 Athmane Madjoudj <athmane@fedoraproject.org> 0.20150122gitbd1b5d0-2
- Use better version (pre-release)
- Include license file in the clients sub-pkg
- Add a license workaround

* Fri Nov 20 2015 Athmane Madjoudj <athmane@fedoraproject.org> 0.bd1b5d0git-1
- Initial spec file.
