# stats.sh
# 2010-06-18
#

output=stats.txt

cd $(dirname "$0")
cd ..
for po in *.po
do
	printf "%10s" "$po: "
	LANG=C msgfmt -c --statistics $po 2>&1
done > $output

# remove temporary files
rm -f messages messages.mo

echo Saved $output
