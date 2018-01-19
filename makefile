#! SHELL=/bin/sh

SUP=/usr/bin/supervisord -c /home/deploy/software/apm/supervisord.conf
CTL_OL=/usr/bin/supervisorctl -c  /home/deploy/software/apm/supervisord.conf
CTL=/usr/bin/supervisorctl

start:
	${CTL} start 'apm:apm-86'{0..9}{0..9}

stop:
	${CTL} stop 'apm:apm-86'{0..9}{0..9}

restart:
	for i in {0..9}; do ${CTL} restart 'apm:apm-86'$${i}$${i}; done

restart_ol:
	for i in {0..9}; do ${CTL_OL} restart 'apm:apm-86'$${i}$${i}; done


update:
	make restart

