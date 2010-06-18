# stats.sh
# 2010-06-18
#

for po in ../*.po
do
	echo -n "$po: "
	LANG=C msgfmt -c --statistics $po
done

# remove temporary files
rm -f messages messages.mo

