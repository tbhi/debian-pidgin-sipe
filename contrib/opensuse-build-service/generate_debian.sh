#!/bin/bash
abort() {
    echo "$0: $1 - Aborting"
    exit 1
}
cleanup() {
    rm -rf debian
    abort "$1"
}

# Sanity checks
version=$(ls pidgin-sipe-*.tar.gz | sed 's/^pidgin-sipe-//;s/.tar.gz$//')
[ -z "${version}" ] && abort "can't find pidgin-sipe archive"
[ -e debian ]       && abort "directory 'debian' - already exists"

# Copy latest source archive
cp pidgin-sipe-${version}.tar.gz pidgin-sipe_${version}.orig.tar.gz

# Extract contrib/debian directory from release
tar --strip-components=2 --wildcards -xvf \
    pidgin-sipe-${version}.tar.gz \
    "*/contrib/debian" || cleanup "tar failed"
[ -e debian ]          || cleanup "directory 'debian' - does not exist"

# Have the contents changed?
if tar 2>/dev/null -df pidgin-sipe_${version}-1.debian.tar.gz; then
    echo "contrib/debian is unchanged - not updating .debian.tar.gz."
else
    # Update debian archive
    tar cfz pidgin-sipe_${version}-1.debian.tar.gz debian || cleanup "can't create tar archive"
fi
rm -rf debian

# Update .dsc files
for p in \
    "Checksums-Sha1=sha1sum" \
    "Checksums-Sha256=sha256sum" \
    "Files=md5sum";
do \
    label=${p%=*}; \
    program=${p#*=}; \
    echo "${label}:"
    for t in \
	pidgin-sipe_${version}.orig.tar.gz \
	pidgin-sipe_${version}-1.debian.tar.gz; \
    do \
	echo " $(${program} ${t} | cut -d' ' -f1) $(wc -c ${t})"; \
    done \
done >checksums.txt
for d in *.dsc; do cat checksums.txt >>${d}; done
rm checksums.txt

# Overwrite those .dsc's that have support for Voice & Video
for os in \
    xUbuntu_11.10; \
do \
    cp pidgin-sipe-VandV.dsc pidgin-sipe-${os}.dsc; \
done

# Overwrite those .dsc's that have support for telepathy
for os in \
    Debian_7.0 \
    xUbuntu_13.10 \
    xUbuntu_13.04 \
    xUbuntu_12.10 \
    xUbuntu_12.04; \
do \
    cp pidgin-sipe-telepathy.dsc pidgin-sipe-${os}.dsc; \
done

# Update SHA-2 256 checksum in Arch Linux PKGBUILD
sed -i -e "s/@@SHA256SUM@@/$(sha256sum pidgin-sipe-${version}.tar.gz | cut -d' ' -f1)/" PKGBUILD

# That's all folks...
echo "Done."
osc status
exit 0
