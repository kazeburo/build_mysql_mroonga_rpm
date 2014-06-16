build mysql56\_mroonga.rpm by Vagrant provisioners

```
$ vagrant up
$ vagrant destroy
$ ls -l rpms-xxxxxxxxxxxx
MySQL-client-5.6.19-1.el6.x86_64.rpm
MySQL-devel-5.6.19-1.el6.x86_64.rpm
MySQL-server-5.6.19-1.el6.x86_64.rpm
MySQL-shared-5.6.19-1.el6.x86_64.rpm
MySQL-shared-compat-5.6.19-1.el6.x86_64.rpm
groonga-devel-4.0.2-1.el6.x86_64.rpm
groonga-libs-4.0.2-1.el6.x86_64.rpm
groonga-normalizer-mysql-1.0.6-1.el6.x86_64.rpm
groonga-normalizer-mysql-devel-1.0.6-1.el6.x86_64.rpm
groonga-tokenizer-mecab-4.0.2-1.el6.x86_64.rpm
mecab-0.996-1.el6.x86_64.rpm
mecab-devel-0.996-1.el6.x86_64.rpm
mecab-ipadic-2.7.0.20070801-8.el6.1.x86_64.rpm
mysql56-mroonga-4.03-2.el6.x86_64.rpm
mysql56-mroonga-doc-4.03-2.el6.x86_64.rpm 
```

To change versions of MySQL and mroonga, edit `provision.sh`


