#!/bin/env python

""" Sample alert code """
# This code checks a RabbitMq message queue to see if messages are backing up.
# Sometimes a RabbitMq subscriber fails and messages start backing up.  
# Use this script to set an alert threshold for backed up messages on a queue.
# Receive email alerts when the message threshold is exceeded.
# code compiled by @yellowpark
# this code is free to use under a GNU Lesser General Public License http://www.gnu.org/licenses/lgpl.html

import amqplib.client_0_8 as amqp
import smtplib
    
# this function sends the ALERT email
def sendmailer ( msgs, q, thresh, subscriber ):    
    # email address to send alert to
    to = 'me@mydomain.com'
    
    # spoof email adress sending the alert email
    sender = 'no-reply@mydomain.com'
    
    #smtp username and password
    smtp_server = 'smtp.mydomain.com'
    smtp_user = 'me@mydomain.com'
    smtp_pwd = 'mypassword'
    
    #smtp details for sending
    smtpserver = smtplib.SMTP(smtp_server,25)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(smtp_user, smtp_pwd)
    
    # construct the message
    header = 'To: %s \nFrom:  %s \nSubject: ALERT - RabbitMq \n' % (to,sender)
    msg = header + '\nRabbitMq has %d messgaes waiting on the message queue: %s.\n\nThe alert threshold for this queue is: %s.\n\nThe subscriber that is consuming this queue is: %s\n\nCheck that the subscriber for this queue is working correctly.' % (msgs,q,thresh,subscriber)
    
    # send the message
    smtpserver.sendmail(smtp_user, to, msg)
    smtpserver.close()
 	
    # print stuff
    print 'email sent!'
    
# Rabbit Server to connect to
host = '127.0.0.1'
port = 5672

# Message alert threshold
msgsPending = 100 # after 100 messages are backed up, an alert email will be sent

# Queue subscriber(s) - enter the name of the subscriber that consumes messages for this queue (you can skip this if you want)
subscriber = 'file_name.py'

# Exchange and queue information
exchange_name = 'the_exchange_name' # change to the exchnge name 
exchange_type = 'direct'
queue_name = 'the_queue_name' # change the queue name to match the actual queue name
routing_key = 'the_routing_key' # change the routing key to match the actual routing key

# Connect to Rabbit - if you have specific settings, define here
connection= amqp.Connection( host ='%s:%s' % ( host, port ),
                        userid = 'userid', # the rabbitMq userid
                        password = 'password', # the rabbitMqpassword
                        ssl = False,
                        virtual_host = '/' )

# Create a channel to talk to Rabbit on
channel = connection.channel()

# Create our exchange
channel.exchange_declare( exchange = exchange_name, 
                          type = exchange_type, 
                          durable = True,
                          auto_delete = False )
# declare the queue                                       
name, jobs, consumers = channel.queue_declare(queue=queue_name, passive=True)

# Close the channel
channel.close()

# Close our connection
connection.close()

# print some stuff
print 'Alert threshold: %d' % (msgsPending)
print 'Queue: %s' % (name)
print 'Jobs: %s' % jobs

if jobs >= msgsPending:
	sendnow = sendmailer(jobs,name,msgsPending,subscriber)
else:
	print 'no email sent!'
