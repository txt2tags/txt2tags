# stats.sh
# 2010-06-18
#

cd $(dirname "$0")
cd ..
for po in *.po
do
	printf "%10s" "$po: "
	LANG=C msgfmt --statistics $po 2>&1
done

# remove temporary files
rm -f messages messages.mo
