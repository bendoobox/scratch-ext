For packaging purposes only, ignore this file.

 * Make sure `stdeb` is installed
 * Update source, whatever
 * Run `python setup.py sdist upload`
 
On deb host
 * update from git repo
 * remove old deb_dist dir
 * python setup.py --command-packages=stdeb.command bdist_deb
 * mv deb_dist/*.deb -> repo dir
 * sudo dpkg-scanpackages binary /dev/null | gzip -9c > binary/Packages.gz