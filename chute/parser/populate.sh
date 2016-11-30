awk '{print 3" "$1}' ./Txt/Games.txt >> BlockSiteList.txt
awk '{print 1" "$1}' ./Txt/Social.txt >> BlockSiteList.txt
awk '{print 2" "$1}' ./Txt/Adult.txt >> BlockSiteList.txt
awk '{print 4" "$1}' ./Txt/Custom.txt >> BlockSiteList.txt
