# pull rabbitmq base image from DOCKER HUB
# FROM rabbitmq:3.6-management

# enable mqtt plugings
# RUN rabbitmq-plugins enable rabbitmq_management
# RUN rabbitmq-plugins enable rabbitmq_mqtt

#COPY rabbitmq-env.conf /etc/rabbitmq/rabbitmq-env.conf
#   COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

#   RUN chown -R rabbitmq:rabbitmq /var/lib/rabbitmq /etc/rabbitmq &&\
#	chmod 777 /var/lib/rabbitmq /etc/rabbitmq


# set user and password of mqtt
# RUN rabbitmqctl add_user mqtt mqtt
# RUN rabbitmqctl set_permissions -p / mqtt ".*" ".*" ".*"
# RUN rabbitmqctl set_user_tags mqtt management

# ENV RABBITMQ_DEFAULT_USER admin
# ENV RABBITMQ_DEFAULT_PASS mypass

# EXPOSE 15672
# EXPOSE 1883




FROM rabbitmq:3.6

ENV RABBITMQ_DEFAULT_USER admin
ENV RABBITMQ_DEFAULT_PASS admin

RUN rabbitmq-plugins enable --offline rabbitmq_management
RUN rabbitmq-plugins enable --offline rabbitmq_mqtt

COPY rabbitmq-env.conf /etc/rabbitmq/rabbitmq-env.conf
COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.config
RUN chown -R rabbitmq:rabbitmq /var/lib/rabbitmq /etc/rabbitmq &&\
	chmod 777 /var/lib/rabbitmq /etc/rabbitmq

EXPOSE 15672
EXPOSE 5672
EXPOSE 1883
