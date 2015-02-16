for php in `ls *.php`
do
    ln -s ./$php /var/www/html/$php
done

for html in `ls *.html`
do
    ln -s ./$html /var/www/html/$html
done
ln -s xunleihao  /var/www/html/xunleihao
