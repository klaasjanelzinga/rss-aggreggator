FROM nginx:1

EXPOSE 80

ENV UPSTREAM_API https://api-ntapdiwuga-ez.a.run.app
ENV UPSTREAM_FRONTEND https://frontend-ntapdiwuga-ez.a.run.app

ADD nginx.conf /etc/nginx/nginx.conf
ADD default.conf.template /var/default.conf.template

CMD envsubst \$PORT  </var/default.conf.template | envsubst \$UPSTREAM_API | envsubst \$UPSTREAM_FRONTEND > /etc/nginx/conf.d/default.conf &&  nginx -g 'daemon off;'