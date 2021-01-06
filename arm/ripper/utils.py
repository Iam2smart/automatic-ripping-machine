#!/usr/bin/env python3
# Collection of utility functions
import os
import sys
import yaml
import logging
import fcntl
import subprocess
import shutil
import requests
import time
import pyudev
import psutil
import apprise
import random
import re
# Added from pull 366
import datetime  # noqa: F401
import psutil  # noqa E402

# from arm.config.config import cfg
from arm.ui import app, db  # noqa E402
from arm.models.models import Track  # noqa: E402


def notify(job, title, body):
    """Send notificaions
     title = title for notification
    body = body of the notification
    """
    # Pushbullet
    # pbul://{accesstoken}
    if job.config.PB_KEY != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # A sample pushbullet notification
            apobj.add('pbul://' + str(job.config.PB_KEY))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending Pushbullet apprise notification.  Continueing processing...")
    # IFTTT
    # ifttt://{WebhookID}@{Event}/
    if job.config.IFTTT_KEY != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # A sample pushbullet notification
            apobj.add('ifttt://' + str(job.config.IFTTT_KEY) + "@" + str(job.config.IFTTT_EVENT))

            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending IFTTT apprise notification.  Continueing processing...")
    # PUSHOVER
    if job.config.PO_USER_KEY != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()

            apobj.add('pover://' + str(job.config.PO_USER_KEY) + "@" + str(job.config.PO_APP_KEY))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending PUSHOVER apprise notification.  continuing  processing...")
    if job.config.APPRISE != "":
        try:
            apprise_notify(job.config.APPRISE, title, body)
            logging.debug("apprise-config: " + str(job.config.APPRISE))
        except Exception as e:  # noqa: E722
            logging.error("Failed sending apprise notification. " + str(e))


def apprise_notify(apprise_cfg, title, body):
    """APPRISE NOTIFICATIONS

    :argument
    apprise_cfg - The full path to the apprise.yaml file
    title - the message title
    body - the main body of the message

    :returns
    nothing
    """
    yaml_file = apprise_cfg
    with open(yaml_file, "r") as f:
        cfg = yaml.load(f)

    cmd = "apprise -vv -t \"{0}\" -b \"{1}\" dbus://".format(title, body)
    cmd1 = "apprise -vv -t \"{0}\" -b \"{1}\" kde://".format(title, body)
    cmd2 = "apprise -vv -t \"{0}\" -b \"{1}\" gnome://".format(title, body)
    cmd3 = "apprise -vv -t \"{0}\" -b \"{1}\" windows://".format(title, body)
    try:
        logging.debug("Trying ##########" + cmd)
        os.system(cmd)
        # subprocess.call(cmd)
    except Exception as e:  # noqa: E722
        logging.error("Failed sending desktops apprise notification. ################ " + str(e))
    try:
        logging.debug("Trying ##########" + cmd1)
        os.system(cmd1)
        # subprocess.call(cmd)
    except Exception as e:  # noqa: E722
        logging.error("Failed sending desktops apprise notification. ################ " + str(e))
    try:
        logging.debug("Trying ##########" + cmd2)
        os.system(cmd2)
        # subprocess.call(cmd)
    except Exception as e:  # noqa: E722
        logging.error("Failed sending desktops apprise notification. ################ " + str(e))
    try:
        logging.debug("Trying ##########" + cmd3)
        os.system(cmd3)
        # subprocess.call(cmd)
    except Exception as e:  # noqa: E722
        logging.error("Failed sending desktops apprise notification. ################ " + str(e))
    # boxcar
    # boxcar://{access_key}/{secret_key}
    if cfg['BOXCAR_KEY'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # A sample pushbullet notification
            apobj.add('boxcar://' + str(cfg['BOXCAR_KEY']) + "/" + str(cfg['BOXCAR_SECRET']))

            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending boxcar apprise notification.  Continueing processing...")
    # discord
    # discord://{WebhookID}/{WebhookToken}/
    if cfg['DISCORD_WEBHOOK_ID'] != "":
        # TODO: add userid to this and config
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # A sample pushbullet notification
            apobj.add('discord://' + str(cfg['DISCORD_WEBHOOK_ID']) + "/" + str(cfg['DISCORD_TOKEN']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending discord apprise notification.  Continueing processing...")
    # Faast
    # faast://{authorizationtoken}
    if cfg['FAAST_TOKEN'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # A sample pushbullet notification
            apobj.add('faast://' + str(cfg['FAAST_TOKEN']))

            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending faast apprise notification.  Continueing processing...")
    # FLOCK
    # flock://{token}/
    if cfg['FLOCK_TOKEN'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # A sample pushbullet notification
            apobj.add('flock://' + str(cfg['FLOCK_TOKEN']))

            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending flock apprise notification.  Continueing processing...")
    # GITTER
    # gitter: // {token} / {room} /
    if cfg['GITTER_TOKEN'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # A sample pushbullet notification
            apobj.add('gitter://' + str(cfg['GITTER_TOKEN']) + "/" + str(cfg['GITTER_ROOM']))

            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending gitter apprise notification.  Continueing processing...")
    # Gotify
    # gotify://{hostname}/{token}
    if cfg['GOTIFY_TOKEN'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # A sample pushbullet notification
            apobj.add('gotify://' + str(cfg['GOTIFY_HOST']) + "/" + str(cfg['GOTIFY_TOKEN']))

            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending gitter apprise notification.  Continueing processing...")
    # Growl
    # growl://{hostname} || growl://{password}@{hostname}
    if cfg['GROWL_HOST'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # Check if we have a pass, use it if we do
            if cfg['GROWL_PASS'] != "":
                # A sample pushbullet notification
                apobj.add('growl://' + str(cfg['GROWL_PASS']) + "@" + str(cfg['GROWL_HOST']))
            else:
                # A sample pushbullet notification
                apobj.add('growl://' + str(cfg['GROWL_HOST']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending growl apprise notification.  Continueing processing...")
    # JOIN
    # join://{apikey}/ ||  join://{apikey}/{device_id}
    if cfg['JOIN_API'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # Check if we have a pass, use it if we do
            if cfg['JOIN_DEVICE'] != "":
                # A sample pushbullet notification
                apobj.add('join://' + str(cfg['JOIN_API']) + "/" + str(cfg['JOIN_DEVICE']))
            else:
                # A sample pushbullet notification
                apobj.add('join://' + str(cfg['JOIN_API']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending growl apprise notification.  Continueing processing...")
    # Kodi
    # kodi://{hostname}:{port} || kodi: // {userid}: {password} @ {hostname}:{port}
    if cfg['KODI_HOST'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # check if we have login details, if so use them
            if cfg['KODI_USER'] != "":
                apobj.add('kodi://' + str(cfg['KODI_USER']) + ":" + str(cfg['KODI_PASS']) + "@" + str(
                    cfg['KODI_HOST']) + ":" + str(cfg['KODI_PORT']))
            else:
                if cfg['KODI_PORT'] != "":
                    # we need to check if they are using secure or this will fail
                    if cfg['KODI_PORT'] == "443":
                        apobj.add('kodis://' + str(cfg['KODI_HOST']) + ":" + str(cfg['KODI_PORT']))
                    else:
                        apobj.add('kodi://' + str(cfg['KODI_HOST']) + ":" + str(cfg['KODI_PORT']))
                else:
                    apobj.add('kodi://' + str(cfg['KODI_HOST']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending KODI apprise notification.  Continueing processing...")
    # KUMULOS
    if cfg['KUMULOS_API'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # A sample pushbullet notification
            apobj.add('kumulos://' + str(cfg['KUMULOS_API']) + "/" + str(cfg['KUMULOS_SERVERKEY']))

            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending KUMULOS apprise notification.  Continueing processing...")
    # LEMETRIC
    if cfg['LAMETRIC_MODE'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()

            # find the correct mode
            if cfg['LAMETRIC_MODE'] == "device":
                apobj.add('lametric://' + str(cfg['LAMETRIC_API']) + "@" + str(cfg['LAMETRIC_HOST']))
            elif cfg['LAMETRIC_MODE'] == "cloud":
                apobj.add('lametric://' + str(cfg['LAMETRIC_APP_ID']) + "@" + str(cfg['LAMETRIC_TOKEN']))
            else:
                logging.error("LAMETRIC apprise LAMETRIC_MODE not set")
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending LAMETRIC apprise notification.  Continueing processing...")
    # MAILGUN
    if cfg['MAILGUN_DOMAIN'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # A sample pushbullet notification
            apobj.add('mailgun://' + str(cfg['MAILGUN_USER']) + "@" + str(cfg['MAILGUN_DOMAIN']) + "/" + str(
                cfg['MAILGUN_APIKEY']))

            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending mailgun apprise notification.  Continueing processing...")
    # MATRIX
    if cfg['MATRIX_HOST'] != "" or cfg['MATRIX_TOKEN'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            if cfg['MATRIX_HOST'] != "":
                apobj.add('matrixs://' + str(cfg['MATRIX_USER']) + ":" + str(cfg['MATRIX_PASS']) + "@" + str(
                    cfg['MATRIX_HOST']))  # + "/#general/#apprise")
            else:
                apobj.add('matrix://' + str(cfg['MATRIX_TOKEN']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending Matrix apprise notification.  Continueing processing...")
    # Microsoft teams
    if cfg['MSTEAMS_TOKENA'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()

            # msteams://{tokenA}/{tokenB}/{tokenC}/
            apobj.add('msteams://' + str(cfg['MSTEAMS_TOKENA']) + "/" + str(cfg['MSTEAMS_TOKENB']) + "/" + str(
                cfg['MSTEAMS_TOKENC']) + "/")

            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending Microsoft teams apprise notification.  Continueing processing...")
    # Nextcloud
    if cfg['NEXTCLOUD_HOST'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()

            apobj.add(
                'nclouds://' + str(cfg['NEXTCLOUD_ADMINUSER']) + ":" + str(cfg['NEXTCLOUD_ADMINPASS']) + "@" + str(
                    cfg['NEXTCLOUD_HOST']) + "/" + str(cfg['NEXTCLOUD_NOTIFY_USER']))

            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending nextcloud apprise notification.  Continueing processing...")
    # Notica
    if cfg['NOTICA_TOKEN'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()

            apobj.add('notica://' + str(cfg['NOTICA_TOKEN']))

            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending notica apprise notification.  Continueing processing...")
    # Notifico
    if cfg['NOTIFICO_PROJECTID'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()

            apobj.add('notica://' + str(cfg['NOTIFICO_PROJECTID']) + "/" + str(cfg['NOTIFICO_MESSAGEHOOK']))

            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending notifico apprise notification.  continuing  processing...")
    # Office365
    if cfg['OFFICE365_TENANTID'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()

            # o365://{tenant_id}:{account_email}/{client_id}/{client_secret}/
            # TODO: we might need to escape/encode the client_secret
            # Replace ? with %3F and  @ with %40
            apobj.add('o365://' + str(cfg['OFFICE365_TENANTID']) + ":" + str(cfg['OFFICE365_ACCOUNTEMAIL']) + "/" + str(
                cfg['OFFICE365_CLIENT_ID']) + "/" + str(cfg['OFFICE365_CLIENT_SECRET']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending Office365 apprise notification.  continuing processing...")
    # Popcorn
    if cfg['POPCORN_API'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            if cfg['POPCORN_EMAIL'] != "":
                apobj.add('popcorn://' + str(cfg['POPCORN_API']) + "/" + str(cfg['POPCORN_EMAIL']))
            if cfg['POPCORN_PHONENO'] != "":
                apobj.add('popcorn://' + str(cfg['POPCORN_API']) + "/" + str(cfg['POPCORN_PHONENO']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending popcorn apprise notification.  Continueing processing...")
    # PROWL
    if cfg['PROWL_API'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            if cfg['PROWL_PROVIDERKEY'] != "":
                apobj.add('prowl://' + str(cfg['PROWL_API']) + "/" + str(cfg['PROWL_PROVIDERKEY']))
            else:
                apobj.add('prowl://' + str(cfg['PROWL_API']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending notifico apprise notification.  continuing  processing...")
    # Pushjet
    # project is dead not worth coding fully
    if cfg['PUSHJET_HOST'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()

            apobj.add('pjet://' + str(cfg['PUSHJET_HOST']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending pushjet apprise notification.  continuing  processing...")
    # techulus push
    if cfg['PUSH_API'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()

            apobj.add('push://' + str(cfg['PUSH_API']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending techulus push apprise notification.  continuing  processing...")
    # PUSHED
    if cfg['PUSHED_APP_KEY'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()

            apobj.add('pushed://' + str(cfg['PUSHED_APP_KEY']) + "/" + str(cfg['PUSHED_APP_SECRET']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending PUSHED apprise notification.  continuing  processing...")
    # PUSHSAFER
    if cfg['PUSHSAFER_KEY'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()

            apobj.add('psafers://' + str(cfg['PUSHSAFER_KEY']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending pushsafer apprise notification.  continuing  processing...")
    # ROCKETCHAT
    # rocket://{webhook}@{hostname}/{@user}
    if cfg['ROCKETCHAT_HOST'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # TODO: Add checks for webhook or default modes
            # for now only the webhook will work
            apobj.add('rocket://' + str(cfg['ROCKETCHAT_WEBHOOK']) + "@" + str(cfg['ROCKETCHAT_HOST']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending rocketchat apprise notification.  continuing  processing...")
    # ryver
    # ryver://{organization}/{token}/
    if cfg['RYVER_ORG'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # TODO: Add checks for webhook or default modes
            # for now only the webhook will work
            apobj.add('ryver://' + str(cfg['RYVER_ORG']) + "/" + str(cfg['RYVER_TOKEN']) + "/")
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending RYVER apprise notification.  continuing  processing...")
    # Sendgrid
    # sendgrid://{apikey}:{from_email}
    if cfg['SENDGRID_API'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # TODO: Add tomail
            apobj.add('sendgrid://' + str(cfg['SENDGRID_API']) + ":" + str(cfg['SENDGRID_FROMMAIL']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending sendgrid apprise notification.  continuing  processing...")
    # simplepush
    # spush://{apikey}/
    if cfg['SIMPLEPUSH_API'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            apobj.add('spush://' + str(cfg['SIMPLEPUSH_API']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending simplepush apprise notification.  continuing  processing...")
    # slacks
    # slack://{tokenA}/{tokenB}/{tokenC}
    if cfg['SLACK_TOKENA'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            apobj.add('slack://' + str(cfg['SLACK_TOKENA']) + "/" + str(cfg['SLACK_TOKENB']) + "/" + str(
                cfg['SLACK_TOKENC']) + "/" + str(cfg['SLACK_CHANNEL']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending slacks apprise notification.  continuing  processing...")
    # SPARKPOST
    # sparkpost://{user}@{domain}/{apikey}/ || sparkpost://{user}@{domain}/{apikey}/{email}/
    if cfg['SPARKPOST_API'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            apobj.add('sparkpost://' + str(cfg['SPARKPOST_USER']) + "@" + str(cfg['SPARKPOST_HOST']) + "/" + str(
                cfg['SPARKPOST_API']) + "/" + str(cfg['SPARKPOST_EMAIL']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending SparkPost apprise notification.  continuing  processing...")
    # spontit
    # spontit://{user}@{apikey}
    if cfg['SPONTIT_API'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            apobj.add('spontit://' + str(cfg['SPONTIT_USER_ID']) + "@" + str(cfg['SPONTIT_API']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending Spontit apprise notification.  continuing  processing...")
    # Telegram
    # tgram://{bot_token}/{chat_id}/ || tgram://{bot_token}/
    if cfg['TELEGRAM_BOT_TOKEN'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            apobj.add('tgram://' + str(cfg['TELEGRAM_BOT_TOKEN']) + "/" + str(cfg['TELEGRAM_CHAT_ID']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending Telegram apprise notification.  continuing  processing...")
    # Twist
    # twist://{email}/{password} || twist://{password}:{email}
    if cfg['TWIST_EMAIL'] != "":
        try:
            # Create an Apprise instance
            # TODO: add channel var and check if its blank
            apobj = apprise.Apprise()
            apobj.add('twist://' + str(cfg['TWIST_EMAIL']) + "/" + str(cfg['TWIST_PASS']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending Twist apprise notification.  continuing  processing...")
    # XBMC
    # xbmc://{userid}:{password}@{hostname}:{port} ||  xbmc://{hostname}:{port}
    if cfg['XBMC_HOST'] != "":
        try:
            # Create an Apprise instance
            # TODO: add channel var and check if its blank
            apobj = apprise.Apprise()
            # if we get user we use the username and pass
            if cfg['XBMC_USER'] != "":
                apobj.add('xbmc://' + str(cfg['XBMC_USER']) + ":" + str(cfg['XBMC_PASS']) + "@" + str(
                    cfg['XBMC_HOST']) + ":" + str(cfg['XBMC_PORT']))
            else:
                apobj.add('xbmc://' + str(cfg['XBMC_HOST']) + ":" + str(cfg['XBMC_PORT']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending XBMC apprise notification.  continuing  processing...")
    # XMPP
    # xmpp://{password}@{hostname}:{port} || xmpps://{userid}:{password}@{hostname}
    if cfg['XMPP_HOST'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()
            # Is the user var filled
            if cfg['XMPP_USER'] != "":
                # xmpps://{userid}:{password}@{hostname}
                apobj.add(
                    'xmpps://' + str(cfg['XMPP_USER']) + ":" + str(cfg['XMPP_PASS']) + "@" + str(cfg['XMPP_HOST']))
            else:
                # xmpp: // {password} @ {hostname}: {port}
                apobj.add('xmpp://' + str(cfg['XMPP_PASS']) + "@" + str(cfg['XMPP_HOST']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending XMPP apprise notification.  continuing  processing...")
    # Webex teams
    # wxteams://{token}/
    if cfg['WEBEX_TEAMS_TOKEN'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()

            apobj.add('wxteams://' + str(cfg['WEBEX_TEAMS_TOKEN']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending Webex teams apprise notification.  continuing  processing...")
    # Zulip
    # zulip://{botname}@{organization}/{token}/
    if cfg['ZILUP_CHAT_TOKEN'] != "":
        try:
            # Create an Apprise instance
            apobj = apprise.Apprise()

            apobj.add('zulip://' + str(cfg['ZILUP_CHAT_BOTNAME']) + "@" + str(cfg['ZILUP_CHAT_ORG']) + "/" + str(
                cfg['ZILUP_CHAT_TOKEN']))
            # Then notify these services any time you desire. The below would
            # notify all of the services loaded into our Apprise object.
            apobj.notify(
                body,
                title=title,
            )
        except:  # noqa: E722
            logging.error("Failed sending Zulip apprise notification.  continuing  processing...")


def detect_disctype(devpath):
    """Parse udev for properties of current disc"""
    disctype = "unknown"
    label = "unknown"
    context = pyudev.Context()
    device = pyudev.Devices.from_device_file(context, devpath)
    return parse_udev(device.items())

def parse_udev_cmdline(args):
    udev = {}
    if args.disctype:
        (k, v) = args.disctype.split('=', 1)
        udev[k] = v
    if args.label:
        (k, v) = args.label.split('=', 1)
        udev[k] = v
    return parse_udev(udev)

def parse_udev(udev_dict):
    map_udev_disctype = {
            "ID_CDROM_MEDIA_BD": "bluray",
            "ID_CDROM_MEDIA_DVD": "dvd",
            "ID_CDROM_MEDIA_TRACK_COUNT_AUDIO": "music"
            }
    disctype == "unknown"
    label = udev_dict.get("ID_FS_LABEL", None)
    if label is None:
        label == "unknown"
    elif label == "iso9660":
        disctype = "data"
    else:
        # check for known disctypes
        for key in map_udev_disctype.keys():
            if key in udev_dict:
                disctype = map_udev_disctype.get(key)
                break
    return (disctype, label)


def eject(devpath):
    """Eject disc on devpath."""
    logging.info("ejecting disc on %s" % devpath)
    os.system("eject %s" % devpath)


def get_pid():
    pid = os.getpid()
    p = psutil.Process(pid)
    return (pid, hash(p))


def scan_emby(job):
    """Trigger a media scan on Emby"""

    if job.config.EMBY_REFRESH:
        logging.info("Sending Emby library scan request")
        url = "http://" + job.config.EMBY_SERVER + ":" + job.config.EMBY_PORT + "/Library/Refresh?api_key=" \
              + job.config.EMBY_API_KEY
        try:
            req = requests.post(url)
            if req.status_code > 299:
                req.raise_for_status()
            logging.info("Emby Library Scan request successful")
        except requests.exceptions.HTTPError:
            logging.error("Emby Library Scan request failed with status code: " + str(req.status_code))
    else:
        logging.info("EMBY_REFRESH config parameter is false.  Skipping emby scan.")


def sleep_check_process(process_str, transcode_limit):
    """ New function to check for max_transcode from cfg file and force obey limits\n
    arguments:
    process_st - The process string from arm.yaml
    transcode_limit - The user defined limit for maximum transcodes\n\n

    returns:
    True - when we have space in the transcode queue
    """
    if transcode_limit > 0:
        loop_count = transcode_limit + 1
        logging.debug("loop_count " + str(loop_count))
        logging.info("Starting A sleep check of " + str(process_str))
        while loop_count >= transcode_limit:
            loop_count = sum(1 for proc in psutil.process_iter() if proc.name() == process_str)
            logging.debug("Number of Processes running is:" + str(loop_count) + " going to waiting 12 seconds.")
            if transcode_limit > loop_count:
                return True
            # Try to make each check at different times
            x = random.randrange(20, 120, 10)
            logging.debug("sleeping for " + str(x) + " seconds")
            time.sleep(x)
    else:
        logging.info("Transcode limit is disabled")


def move_files(basepath, filename, job, ismainfeature=False):
    """Move files into final media directory\n
    basepath = path to source directory\n
    filename = name of file to be moved\n
    job = instance of Job class\n
    ismainfeature = True/False"""
    # TODO update this to use prettytables
    logging.debug("Moving files: " + str(job))

    if job.title_manual:
        # logging.info("Found new title: " + job.new_title + " (" + str(job.new_year) + ")")
        # videotitle = job.new_title + " (" + str(job.new_year) + ")"
        hasnicetitle = True
    else:
        hasnicetitle = job.hasnicetitle

    videotitle = job.title + " (" + str(job.year) + ")"

    logging.debug(
        "Arguments: " + basepath + " : " + filename + " : " + str(hasnicetitle) + " : " + videotitle + " : " + str(
            ismainfeature))

    if hasnicetitle:
        m_path = os.path.join(job.config.MEDIA_DIR + videotitle)

        if not os.path.exists(m_path):
            logging.info("Creating base title directory: " + m_path)
            os.makedirs(m_path)

        if ismainfeature is True:
            logging.info("Track is the Main Title.  Moving '" + filename + "' to " + m_path)

            m_file = os.path.join(m_path, videotitle + "." + job.config.DEST_EXT)
            if not os.path.isfile(m_file):
                try:
                    shutil.move(os.path.join(basepath, filename), m_file)
                except shutil.Error:
                    logging.error("Unable to move '" + filename + "' to " + m_path)
            else:
                logging.info("File: " + m_file + " already exists.  Not moving.")
        else:
            e_path = os.path.join(m_path, job.config.EXTRAS_SUB)

            if not os.path.exists(e_path):
                logging.info("Creating extras directory " + e_path)
                os.makedirs(e_path)

            logging.info("Moving '" + filename + "' to " + e_path)

            e_file = os.path.join(e_path, videotitle + "." + job.config.DEST_EXT)
            if not os.path.isfile(e_file):
                try:
                    shutil.move(os.path.join(basepath, filename), os.path.join(e_path, filename))
                except shutil.Error:
                    logging.error("Unable to move '" + filename + "' to " + e_path)
            else:
                logging.info("File: " + e_file + " already exists.  Not moving.")

    else:
        logging.info("hasnicetitle is false.  Not moving files.")


def rename_files(oldpath, job):
    """
    Rename a directory and its contents based on job class details\n
    oldpath = Path to existing directory\n
    job = An instance of the Job class\n

    returns new path if successful
    """
    # Check if the job has a nice title after rip is complete, if so use the media dir not the arm
    # This is for media that was recognised after the wait period/disk started ripping
    if job.hasnicetitle:
        newpath = os.path.join(job.config.MEDIA_DIR, job.title + " (" + str(job.year) + ")")
    else:
        newpath = os.path.join(job.config.ARMPATH, job.title + " (" + str(job.year) + ")")

    logging.debug("oldpath: " + oldpath + " newpath: " + newpath)
    logging.info("Changing directory name from " + oldpath + " to " + newpath)

    # Added from pull 366 Sometimes a job fails, after the rip, but before move of the tracks into the folder,
    # at which point the below command will move the newly ripped folder inside the old correctly named folder. This
    # can be a problem as the job when it tries to move the files, won't find them. other than putting in an error
    # message, I'm not sure how to permanently fix this problem. Maybe I could add a configurable option for deletion
    # of crashed job files?
    if os.path.isdir(newpath):
        logging.info(
            "Error: The 'new' directory already exists, "
            "ARM will probably copy the newly ripped folder into the old-new folder.")

    try:
        shutil.move(oldpath, newpath)
        logging.debug("Directory name change successful")
    except shutil.Error:
        logging.info("Error change directory from " + oldpath + " to " + newpath + ".  Likely the path already exists.")
        raise OSError(2, 'No such file or directory', newpath)

    return newpath


def make_dir(path):
    """
Make a directory\n
    path = Path to directory\n

    returns success True if successful
        false if the directory already exists
    """
    if not os.path.exists(path):
        logging.debug("Creating directory: " + path)
        try:
            os.makedirs(path)
            return True
        except OSError:
            err = "Couldn't create a directory at path: " + path + " Probably a permissions error.  Exiting"
            logging.error(err)
            sys.exit(err)
            # return False
    else:
        return False


def get_cdrom_status(devpath):
    """get the status of the cdrom drive\n
    devpath = path to cdrom\n

    returns int
    CDS_NO_INFO		0\n
    CDS_NO_DISC		1\n
    CDS_TRAY_OPEN		2\n
    CDS_DRIVE_NOT_READY	3\n
    CDS_DISC_OK		4\n

    see linux/cdrom.h for specifics\n
    """
    result = -1 # unknown
    try:
        fd = os.open(devpath, os.O_RDONLY | os.O_NONBLOCK)
        result = fcntl.ioctl(fd, 0x5326, 0)
    except Exception as e:
        logging.error("Failed to check status of device %s: %s" % (devpath, e))

    return result

def is_cdrom_ready(devpath):
    return get_cdrom_status(devpath) == 4

def find_file(filename, search_path):
    """
    Check to see if file exists by searching a directory recursively\n
    filename = filename to look for\n
    search_path = path to search recursively\n

    returns True or False
    """

    for dirpath, dirnames, filenames in os.walk(search_path):
        if filename in filenames:
            return True
    return False


def rip_music(job, logfile):
    """
    Rip music CD using abcde using abcde config\n
    job = job object\n
    logfile = location of logfile\n

    returns True/False for success/fail
    """

    abcfile = job.config.ABCDE_CONFIG_FILE  # cfg['ABCDE_CONFIG_FILE']
    if job.disctype == "music":
        logging.info("Disc identified as music")
        # If user has set a cfg file with ARM use it
        if os.path.isfile(abcfile):
            cmd = 'abcde -d "{0}" -c {1} >> "{2}" 2>&1'.format(
                job.devpath,
                abcfile,
                logfile
            )
        else:
            cmd = 'abcde -d "{0}" >> "{1}" 2>&1'.format(
                job.devpath,
                logfile
            )

        logging.debug("Sending command: " + cmd)

        try:
            subprocess.check_output(
                cmd,
                shell=True
            ).decode("utf-8")
            logging.info("abcde call successful")
            return True
        except subprocess.CalledProcessError as ab_error:
            err = "Call to abcde failed with code: " + str(ab_error.returncode) + "(" + str(ab_error.output) + ")"
            logging.error(err)
            # sys.exit(err)

    return False


def rip_data(job, datapath, logfile):
    """
    Rip data disc using dd on the command line\n
    job = job object\n
    datapath = path to copy data to\n
    logfile = location of logfile\n

    returns True/False for success/fail
    """

    if job.disctype == "data":
        logging.info("Disc identified as data")

        if job.label == "" or job.label is None:
            job.label = "datadisc"

        incomplete_filename = os.path.join(datapath, job.label + ".part")
        final_filename = os.path.join(datapath, job.label + ".iso")

        logging.info("Ripping data disc to: " + incomplete_filename)

        # Added from pull 366
        cmd = 'dd if="{0}" of="{1}" {2} 2>> {3}'.format(
            job.devpath,
            incomplete_filename,
            job.config.DATA_RIP_PARAMETERS,
            logfile
        )

        logging.debug("Sending command: " + cmd)

        try:
            subprocess.check_output(
                cmd,
                shell=True
            ).decode("utf-8")
            logging.info("Data rip call successful")
            os.rename(incomplete_filename, final_filename)
            return True
        except subprocess.CalledProcessError as dd_error:
            err = "Data rip failed with code: " + str(dd_error.returncode) + "(" + str(dd_error.output) + ")"
            logging.error(err)
            os.unlink(incomplete_filename)
            # sys.exit(err)

    return False


def set_permissions(job, directory_to_traverse):
    try:
        corrected_chmod_value = int(str(job.config.CHMOD_VALUE), 8)
        logging.info("Setting permissions to: " + str(job.config.CHMOD_VALUE) + " on: " + directory_to_traverse)
        os.chmod(directory_to_traverse, corrected_chmod_value)

        for dirpath, l_directories, l_files in os.walk(directory_to_traverse):
            for cur_dir in l_directories:
                logging.debug("Setting path: " + cur_dir + " to permissions value: " + str(job.config.CHMOD_VALUE))
                os.chmod(os.path.join(dirpath, cur_dir), corrected_chmod_value)
            for cur_file in l_files:
                logging.debug("Setting file: " + cur_file + " to permissions value: " + str(job.config.CHMOD_VALUE))
                os.chmod(os.path.join(dirpath, cur_file), corrected_chmod_value)
        return True
    except Exception as e:
        err = "Permissions setting failed as: " + str(e)
        logging.error(err)
        return False


def check_db_version(install_path, db_file):
    """
    Check if db exists and is up to date.
    If it doesn't exist create it.  If it's out of date update it.
    """
    from alembic.script import ScriptDirectory
    from alembic.config import Config
    import sqlite3
    import flask_migrate

    # db_file = job.config.DBFILE
    mig_dir = os.path.join(install_path, "arm/migrations")

    config = Config()
    config.set_main_option("script_location", mig_dir)
    script = ScriptDirectory.from_config(config)

    # create db file if it doesn't exist
    if not os.path.isfile(db_file):
        logging.info("No database found.  Initializing arm.db...")
        make_dir(os.path.dirname(db_file))
        with app.app_context():
            flask_migrate.upgrade(mig_dir)

        if not os.path.isfile(db_file):
            logging.error("Can't create database file.  This could be a permissions issue.  Exiting...")
            sys.exit()

    # check to see if db is at current revision
    head_revision = script.get_current_head()
    logging.debug("Head is: " + head_revision)

    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute("SELECT {cn} FROM {tn}".format(cn="version_num", tn="alembic_version"))
    db_version = c.fetchone()[0]
    logging.debug("Database version is: " + db_version)
    if head_revision == db_version:
        logging.info("Database is up to date")
    else:
        logging.info(
            "Database out of date. Head is " + head_revision + " and database is " + db_version
            + ".  Upgrading database...")
        with app.app_context():
            ts = round(time.time() * 100)
            logging.info("Backuping up database '" + db_file + "' to '" + db_file + str(ts) + "'.")
            shutil.copy(db_file, db_file + "_" + str(ts))
            flask_migrate.upgrade(mig_dir)
        logging.info("Upgrade complete.  Validating version level...")

        c.execute("SELECT {cn} FROM {tn}".format(tn="alembic_version", cn="version_num"))
        db_version = c.fetchone()[0]
        logging.debug("Database version is: " + db_version)
        if head_revision == db_version:
            logging.info("Database is now up to date")
        else:
            logging.error(
                "Database is still out of date. Head is " + head_revision + " and database is " + db_version
                + ".  Exiting arm.")
            sys.exit()


def put_track(job, t_no, seconds, aspect, fps, mainfeature, source, filename=""):
    """
    Put data into a track instance\n


    job = job ID\n
    t_no = track number\n
    seconds = lenght of track in seconds\n
    aspect = aspect ratio (ie '16:9')\n
    fps = frames per second (float)\n
    mainfeature = True/False\n
    source = Source of information\n
    filename = filename of track\n
    """

    logging.debug("Track #" + str(t_no) + " Length: " + str(seconds) + " fps: " + str(fps) + " aspect: " + str(
        aspect) + " Mainfeature: " +
                  str(mainfeature) + " Source: " + source)

    t = Track(
        job_id=job.job_id,
        track_number=t_no,
        length=seconds,
        aspect_ratio=aspect,
        # blocks=b,
        fps=fps,
        main_feature=mainfeature,
        source=source,
        basename=job.title,
        filename=filename
    )
    db.session.add(t)
    db.session.commit()


def arm_setup():
    """
    setup arm - make sure everything is fully setup and ready and there are no errors. This is still in dev. ATM

    :arguments
    None

    :return
    None
    """
    from arm.config.config import cfg
    try:
        # Make the ARM dir if it doesnt exist
        if not os.path.exists(cfg['ARMPATH']):
            os.makedirs(cfg['ARMPATH'])
        # Make the RAW dir if it doesnt exist
        if not os.path.exists(cfg['RAWPATH']):
            os.makedirs(cfg['RAWPATH'])
        # Make the Media dir if it doesnt exist
        if not os.path.exists(cfg['MEDIA_DIR']):
            os.makedirs(cfg['MEDIA_DIR'])
        # Make the log dir if it doesnt exist
        if not os.path.exists(cfg['LOGPATH']):
            os.makedirs(cfg['LOGPATH'])
    except IOError as e:  # noqa: F841
        # logging.error("A fatal error has occurred.  Cant find/create the folders from arm.yaml " + str(e))
        # notify(job, "ARM notification", "ARM encountered a fatal error processing " + str(job.title) + ". Check the
        # logs for more details. " + str(e))
        sys.exit(e)


def makecleanlogfile(logfile):
    """
    Clean the log of secret keys and return the removed string

    arguments:
    logfile - the log as string

    returns - a clean string with all keys and api secrets removed
    """
    # TODO: make this cleaner/smaller
    # lets make sure we are using a string
    logfile = str(logfile)
    # logging.debug("inside makecleanlogfile: " + str(logfile) + "\n\r")
    out = re.sub("\(PB_KEY=.*?\)", '(PB_KEY=** REMOVED **)', logfile)  # noqa W605
    out = re.sub("\(EMBY_PASSWORD=.*?\)", '(EMBY_PASSWORD=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(EMBY_API_KEY=.*?\)", '(EMBY_API_KEY=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(EMBY_SERVER=.*?\)", '(EMBY_SERVER=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(IFTTT_KEY=.*?\)", '(IFTTT_KEY=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(OMDB_API_KEY=.*?\)", '(OMDB_API_KEY=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(PO_APP_KEY=.*?\)", '(PO_APP_KEY=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(PO_USER_KEY=.*?\)", '(PO_USER_KEY=** REMOVED **)', out)  # noqa W605
    # \(WEBSERVER_IP=(.*?)\.3[0-9]{1,3}\.[0-9]{1,3}\)
    ips = re.search('\(WEBSERVER_IP=(.*?)\.[0-9]{1,3}\.[0-9]{1,3}\)', out)  # noqa W605
    if ips:
        ip = ips.group(1)
        out = re.sub("\(WEBSERVER_IP=.*?\)", '(WEBSERVER_IP=' + str(ip) + '.xx.xx)', out)  # noqa W605

    # Apprise notifications
    out = re.sub("\(DISCORD_WEBHOOK_ID=.*?\)", '(DISCORD_WEBHOOK_ID=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(DISCORD_TOKEN=.*?\)", '(DISCORD_TOKEN=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(FAAST_TOKEN=.*?\)", '(FAAST_TOKEN=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(FLOCK_TOKEN=.*?\)", '(FLOCK_TOKEN=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(GITTER_TOKEN=.*?\)", '(GITTER_TOKEN=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(GOTIFY_HOST=.*?\)", '(GOTIFY_HOST=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(GROWL_HOST=.*?\)", '(GROWL_HOST=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(GROWL_PASS=.*?\)", '(GROWL_PASS=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(JOIN_API=.*?\)", '(JOIN_API=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(JOIN_DEVICE=.*?\)", '(JOIN_DEVICE=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(KODI_HOST=.*?\)", '(KODI_HOST=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(KODI_PASS=.*?\)", '(KODI_PASS=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(KUMULOS_API=.*?\)", '(KUMULOS_API=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(LAMETRIC_API=.*?\)", '(LAMETRIC_API=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(LAMETRIC_HOST=.*?\)", '(LAMETRIC_HOST=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(LAMETRIC_APP_ID=.*?\)", '(LAMETRIC_APP_ID=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(LAMETRIC_TOKEN=.*?\)", '(LAMETRIC_TOKEN=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(MAILGUN_DOMAIN=.*?\)", '(MAILGUN_DOMAIN=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(MAILGUN_APIKEY=.*?\)", '(MAILGUN_APIKEY=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(MATRIX_HOST=.*?\)", '(MATRIX_HOST=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(MATRIX_PASS=.*?\)", '(MATRIX_PASS=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(MATRIX_TOKEN=.*?\)", '(MATRIX_TOKEN=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(MSTEAMS_TOKENA=.*?\)", '(MSTEAMS_TOKENA=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(MSTEAMS_TOKENB=.*?\)", '(MSTEAMS_TOKENB=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(MSTEAMS_TOKENC=.*?\)", '(MSTEAMS_TOKENC=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(NEXTCLOUD_HOST=.*?\)", '(NEXTCLOUD_HOST=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(NEXTCLOUD_ADMINPASS=.*?\)", '(NEXTCLOUD_ADMINPASS=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(NOTICA_TOKEN=.*?\)", '(NOTICA_TOKEN=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(NOTIFICO_PROJECTID=.*?\)", '(NOTIFICO_PROJECTID=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(NOTIFICO_MESSAGEHOOK=.*?\)", '(NOTIFICO_MESSAGEHOOK=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(OFFICE365_TENANTID=.*?\)", '(OFFICE365_TENANTID=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(OFFICE365_CLIENT_ID=.*?\)", '(OFFICE365_CLIENT_ID=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(OFFICE365_CLIENT_SECRET=.*?\)", '(OFFICE365_CLIENT_SECRET=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(POPCORN_API=.*?\)", '(POPCORN_API=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(POPCORN_EMAIL=.*?\)", '(POPCORN_EMAIL=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(POPCORN_PHONENO=.*?\)", '(POPCORN_PHONENO=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(PROWL_API=.*?\)", '(PROWL_API=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(PROWL_PROVIDERKEY=.*?\)", '(PROWL_PROVIDERKEY=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(PUSH_API=.*?\)", '(PUSH_API=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(PUSHED_APP_KEY=.*?\)", '(PUSHED_APP_KEY=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(PUSHED_APP_SECRET=.*?\)", '(PUSHED_APP_SECRET=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(PUSHSAFER_KEY=.*?\)", '(PUSHSAFER_KEY=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(ROCKETCHAT_HOST=.*?\)", '(ROCKETCHAT_HOST=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(ROCKETCHAT_PASS=.*?\)", '(ROCKETCHAT_PASS=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(ROCKETCHAT_WEBHOOK=.*?\)", '(ROCKETCHAT_WEBHOOK=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(RYVER_ORG=.*?\)", '(RYVER_ORG=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(RYVER_TOKEN=.*?\)", '(RYVER_TOKEN=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(SENDGRID_API=.*?\)", '(SENDGRID_API=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(SENDGRID_FROMMAIL=.*?\)", '(SENDGRID_FROMMAIL=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(SIMPLEPUSH_API=.*?\)", '(SIMPLEPUSH_API=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(SLACK_TOKENA=.*?\)", '(SLACK_TOKENA=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(SLACK_TOKENB=.*?\)", '(SLACK_TOKENB=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(SLACK_TOKENC=.*?\)", '(SLACK_TOKENC=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(SPARKPOST_API=.*?\)", '(SPARKPOST_API=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(SPARKPOST_HOST=.*?\)", '(SPARKPOST_HOST=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(SPONTIT_API=.*?\)", '(SPONTIT_API=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(SPONTIT_USER_ID=.*?\)", '(SPONTIT_USER_ID=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(TELEGRAM_BOT_TOKEN=.*?\)", '(TELEGRAM_BOT_TOKEN=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(TELEGRAM_CHAT_ID=.*?\)", '(TELEGRAM_CHAT_ID=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(TWIST_EMAIL=.*?\)", '(TWIST_EMAIL=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(TWIST_PASS=.*?\)", '(TWIST_PASS=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(XBMC_HOST=.*?\)", '(XBMC_HOST=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(XBMC_PASS=.*?\)", '(XBMC_PASS=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(XMPP_HOST=.*?\)", '(XMPP_HOST=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(XMPP_PASS=.*?\)", '(XMPP_PASS=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(WEBEX_TEAMS_TOKEN=.*?\)", '(WEBEX_TEAMS_TOKEN=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(ZILUP_CHAT_TOKEN=.*?\)", '(ZILUP_CHAT_TOKEN=** REMOVED **)', out)  # noqa W605
    out = re.sub("\(ZILUP_CHAT_ORG=.*?\)", '(ZILUP_CHAT_ORG=** REMOVED **)', out)  # noqa W605
    # format for more entries
    # out = re.sub("\(CONFIG_ID=.*?\)", '(CONFIG_ID=** REMOVED **)', out)

    # logging.debug("our clean log string" + str(out))
    return out


def database_updater(args, job, wait_time=90):
    """
    Try to update our db for x seconds and handle it nicely if we cant

    :param args:
    :param job:
    :param wait_time:
    :return:
    """
    # Loop through our args and try to set any of our job variables
    for (key, value) in args.items():
        logging.debug(str(key) + "= " + str(value))
        logging.debug("key = " + str(key))
        if key == "job_id":
            job.job_id = value
        elif key == "logfile":
            job.logfile = value
        elif key == "status":
            job.status = value
        elif key == "no_of_titles":
            job.no_of_titles = value
        elif key == "job_length":
            job.job_length = value
        elif key == "crc_id":
            job.crc_id = value
        elif key == "year":
            job.year = value
        elif key == "year_auto":
            job.year_auto = value
        elif key == "year_manual":
            job.year_manual = value
        elif key == "no_of_titles":
            job.no_of_titles = value
        elif key == "title":
            job.title = value
        elif key == "title_auto":
            job.title_auto = value
        elif key == "title_manual":
            job.title_manual = value
        elif key == "video_type":
            job.video_type = value
        elif key == "video_type_auto":
            job.video_type_auto = value
        elif key == "video_type_manual":
            job.video_type_manual = value
        elif key == "imdb_id":
            job.imdb_id = value
        elif key == "imdb_id_auto":
            job.poster_url = value
        elif key == "imdb_id_manual":
            job.imdb_id_manual = value
        elif key == "poster_url":
            job.poster_url = value
        elif key == "poster_url_auto":
            job.poster_url_auto = value
        elif key == "poster_url_manual":
            job.poster_url_manual = value
        elif key == "hasnicetitle":
            job.hasnicetitle = value
        elif key == "errors":
            job.errors = value

    for i in range(wait_time):  # give up after the users wait period in seconds
        try:
            db.session.commit()
        except Exception as e:
            if "locked" in str(e):
                time.sleep(1)
                logging.debug("database is locked - trying in 1 second")
            else:
                logging.debug("Error: " + str(e))
                raise RuntimeError(str(e))
        else:
            logging.debug("successfully written to the database")
            return True
