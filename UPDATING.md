For packaging purposes only, ignore this file.

 * Make sure `stdeb` is installed
 * Update source, whatever
 * Run `python setup.py sdist upload`
 
On deb host
 * update from git repo
 * remove old deb_dist dir
 * python setup.py --command-packages=stdeb.command bdist_deb
 * mv deb_dist/*.deb [repo_dir]/dists/bendoobox/main/binary-armhf/.
 * cd [repo_dir]
 * sudo dpkg-scanpackages dists /dev/null > /tmp/Packages;bzip2 -f /tmp/Packages;sudo mv /tmp/Packages.bz2 ./dists/bendoobox/main/binary-armhf/.
