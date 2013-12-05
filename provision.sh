#!/bin/sh

MYSQL_VER="5.6.15-1"
MROONGA_VER="3.10-1"

yum -y groupinstall 'Development Tools'
yum -y install http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
yum -y install wget yum-utils
yum -y remove mysql mysql-server
if [ -d /var/lib/mysql ]; then
  rm -rf /var/lib/mysql
fi
if [ -d /tmp/build ]; then
  rm -rf /tmp/build
fi

mkdir -p /tmp/build/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
echo '%_topdir /tmp/build/rpmbuild' > /root/.rpmmacros
echo '%debug_package %{nil}' >> /root/.rpmmacros

mkdir -p /tmp/build/rpmbuild/RPMS/x86_64
cd /tmp/build/rpmbuild/RPMS/x86_64
echo "Download MySQL packages.."
wget --progress=bar:force http://ftp.jaist.ac.jp/pub/mysql/Downloads/MySQL-5.6/MySQL-shared-compat-$MYSQL_VER.el6.x86_64.rpm \
  http://ftp.jaist.ac.jp/pub/mysql/Downloads/MySQL-5.6/MySQL-shared-$MYSQL_VER.el6.x86_64.rpm \
  http://ftp.jaist.ac.jp/pub/mysql/Downloads/MySQL-5.6/MySQL-server-$MYSQL_VER.el6.x86_64.rpm \
  http://ftp.jaist.ac.jp/pub/mysql/Downloads/MySQL-5.6/MySQL-devel-$MYSQL_VER.el6.x86_64.rpm \
  http://ftp.jaist.ac.jp/pub/mysql/Downloads/MySQL-5.6/MySQL-client-$MYSQL_VER.el6.x86_64.rpm 
yum -y localinstall MySQL-shared-compat-5*
yum -y localinstall MySQL-shared-5* MySQL-server-5* MySQL-devel-5* MySQL-client-5*
cd /tmp/build/rpmbuild/SRPMS
wget --progress=bar:force http://ftp.jaist.ac.jp/pub/mysql/Downloads/MySQL-5.6/MySQL-$MYSQL_VER.el6.src.rpm
rpm -Uvh MySQL-$MYSQL_VER.el6.src.rpm

/etc/init.d/mysql start
sleep 3
mysqladmin -uroot --password=$(head -1 /root/.mysql_secret | awk -F ': ' '{print $2}') password ""
mysql -uroot -e 'update user SET Password="" where User="root"' mysql

yum -y install http://packages.groonga.org/centos/groonga-release-1.1.0-1.noarch.rpm
yum -y install groonga-libs groonga-devel \
  groonga-normalizer-mysql groonga-normalizer-mysql-devel \
  gperf ncurses-devel time zlib-devel

cd /tmp/build
wget --progress=bar:force http://packages.groonga.org/centos/6/source/SRPMS/mysql-mroonga-$MROONGA_VER.el6.src.rpm
rpm -ivh mysql-mroonga-*.src.rpm

cd /tmp/build/rpmbuild/SPECS
cp mysql-mroonga.spec mysql56-mroonga.spec
MYSQL_RPM_VER=$(rpm -qa|grep MySQL-server|awk -F '-' '{print $3}')
MYSQL_RPM_REL=$(rpm -qa|grep MySQL-server|awk -F '-' '{print $4}'|awk -F '.' '{print $1}')
MYSQL_RPM_DIST=$(rpm -qa|grep MySQL-server|awk -F '-' '{print $4}'|awk -F '.' '{print $2}')
perl -i -pe "s/mysql_version_default\s+5\.6\.[0-9]+$/mysql_version_default $MYSQL_RPM_VER/g" mysql56-mroonga.spec
perl -i -pe "s/mysql_release_default\s+[a-z0-9\-_]+$/mysql_release_default $MYSQL_RPM_REL/g" mysql56-mroonga.spec
perl -i -pe "s/mysql_dist_default\s+[a-z0-9\-_]+$/mysql_dist_default $MYSQL_RPM_DIST/g" mysql56-mroonga.spec
perl -i -pe "s/mysql_spec_file_default\s+mysql\..+\.spec$/mysql_spec_file_default mysql.spec/g" mysql56-mroonga.spec
perl -i -pe "s/^Name:\s+mysql-mroonga$/Name: mysql56-mroonga/" mysql56-mroonga.spec
cd ..
rpmbuild -bb SPECS/mysql56-mroonga.spec

echo "rpmbuild DONE. move to shared folder"

DATENOW=$(date +%Y%m%d%H%M)
cd /vagrant
mkdir rpms-$DATENOW
cd rpms-$DATENOW
yumdownloader --disablerepo=* --enablerepo=groonga groonga-devel groonga-libs groonga-normalizer-mysql \
  groonga-normalizer-mysql-devel groonga-tokenizer-mecab mecab mecab-devel mecab-ipadic
cp /tmp/build/rpmbuild/RPMS/x86_64/*.rpm ./
rm -f MySQL-test-* MySQL-embedded-*

echo "Done!!"



