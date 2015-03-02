For packaging purposes only, ignore this file.

 * Make sure `stdeb` is installed
 * Update source, whatever
 * Run `python setup.py sdist upload`
 
On deb host
 * pypi-download scratch-ext
 * py2dsc-deb [version].tar.gz
 * mv deb_dist/*.deb -> repo dir
 * sudo dpkg-scanpackages binary /dev/null | gzip -9c > binary/Packages.gz