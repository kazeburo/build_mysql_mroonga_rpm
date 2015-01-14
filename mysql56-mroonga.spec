%define mysql_version <MYSQL_RPM_VER>
%define mysql_release <MYSQL_RPM_REL>
%define mysql_dist    <MYSQL_RPM_DIST>
%define mysql_download_base_url http://ftp.jaist.ac.jp/pub/mysql/Downloads/MySQL-5.6
%define mysql_spec_file mysql.spec

%define groonga_required_version 4.0.0

Name:           mysql56-mroonga
Version:        <VERSION>
Release:        <REL>%{?dist}
Summary:        A fast fulltext searchable storage engine for MySQL

Group:          Applications/Databases
License:        LGPLv2.1
URL:            http://mroonga.org/
Source0:        http://packages.groonga.org/source/mroonga/mroonga-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
BuildRequires:  groonga-devel >= %{groonga_required_version}
BuildRequires:  groonga-normalizer-mysql-devel
BuildRequires:  wget
BuildRequires:  which
BuildRequires:  MySQL-devel
Requires:       MySQL-server = %{mysql_version}-%{mysql_release}.%{mysql_dist}
Requires:       MySQL-client = %{mysql_version}-%{mysql_release}.%{mysql_dist}
Requires:       groonga-libs >= %{groonga_required_version}
Requires:       groonga-normalizer-mysql
Patch0:         mroonga-409.patch

%description
Mroonga is a fast fulltext searchable storage plugin for MySQL.
It is based on Groonga that is a fast fulltext search engine and
column store. Groonga is good at real-time update.

%package doc
Summary:        Documentation for Mroonga
Group:          Documentation
License:        LGPLv2.1

%description doc
Documentation for Mroonga

%prep
%setup -q -n mroonga-%{version}
%patch0 -p1

mysql_full_version=%{mysql_version}-%{mysql_release}.%{mysql_dist}
srpm=MySQL-${mysql_full_version}.src.rpm
if [ ! -f ../../SRPMS/$srpm ]; then
    wget --continue -O ../../SRPMS/$srpm %{mysql_download_base_url}/$srpm
    rpm -Uvh ../../SRPMS/$srpm
    for package in client devel embedded server shared test; do
        rpm=MySQL-${package}-${mysql_full_version}.%{_arch}.rpm
	mkdir -p ../../RPMS/%{_arch}
	if [ ! -f ../../RPMS/%{_arch}/$rpm ]; then
            wget --continue -O ../../RPMS/%{_arch}/$rpm \
		%{mysql_download_base_url}/$rpm
	fi
    done
fi
if ! rpm -q MySQL-devel 2>&1 | grep $mysql_full_version > /dev/null; then
    rpm=../../RPMS/%{_arch}/MySQL-devel-$mysql_full_version.%{_arch}.rpm
    sudo rpm -Uvh $rpm || \
	echo "install MySQL-devel by hand: sudo rpm -Uvh $(pwd)/$rpm" && \
	exit 1
fi

%build
mysql_source=../mysql-%{mysql_version}/mysql-%{mysql_version}
if [ ! -d ${mysql_source} ]; then
    specs_dir=
    MYSQL_RPMBUILD_TEST=no rpmbuild -bp \
	--define 'runselftest 0' \
        --define 'optflags -O0' \
	../../SPECS/%{mysql_spec_file}
fi
%configure --disable-static --with-mysql-source=${mysql_source} \
    %{?mroonga_configure_options}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/mysql/plugin/*.la
mv $RPM_BUILD_ROOT%{_datadir}/doc/mroonga/ mysql-mroonga-doc/

%clean
rm -rf $RPM_BUILD_ROOT

%post
mysql_command=`which mysql`
password_option=""
$mysql_command -u root -e "quit"
if [ $? -ne 0 ]; then
    password_option="-p"
fi
current_version=0
version=`echo %{groonga_required_version} | sed -e 's/\.//g'`
required_version=`expr $version`
version=`$mysql_command -e "SHOW VARIABLES LIKE 'mroonga_libgroonga_version'" | \
    grep mroonga | cut -f 2 | sed -e 's/\.//g'`
if [ -n "$version" ]; then
    current_version=`expr $version`
fi
install_sql=%{_datadir}/mroonga/install.sql
uninstall_sql=%{_datadir}/mroonga/uninstall.sql

if [ "$1" = 2 ] ; then
    if [ $current_version -lt $required_version ]; then
    command="$mysql_command -u root $password_option"
    echo "run the following command after restarting MySQL server:";
    echo "  $command < ${uninstall_sql}"
    echo "  $command < ${install_sql}"
    exit 0
    else
    command="$mysql_command -u root $password_option < ${uninstall_sql}"
    echo $command
    eval $command || \
        (echo "run the following command to unregister Mroonga:"; \
         echo "  $command")
    fi
fi
command="$mysql_command -u root $password_option < ${install_sql}"
echo $command
eval $command || \
    (echo "run the following command to register Mroonga:"; \
     echo "  $command")


%preun
uninstall_sql=%{_datadir}/mroonga/uninstall.sql
mysql_command=`which mysql`
if $mysql_command -u root -e "quit"; then
    password_option=""
else
    password_option="-p"
fi
if [ "$1" = 0 ]; then
    command="$mysql_command -u root $password_option < ${uninstall_sql}"
    echo $command
    eval $command || \
    (echo "run the following command to unregister Mroonga:"; \
     echo "  $command")
fi


%files
%defattr(-,root,root,-)
%{_libdir}/mysql/plugin/
%{_datadir}/man/man1/*
%{_datadir}/man/*/man1/*
%{_prefix}/share/mroonga/*.sql

%files doc
%defattr(-,root,root,-)
%doc README COPYING
%doc mysql-mroonga-doc/*

%changelog






